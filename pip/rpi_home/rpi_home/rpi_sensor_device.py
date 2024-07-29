from __future__ import annotations

import os
import time
import socket
import logging
from typing import Any


from .version import RPI_HOME_VERSION
from .const import RPI_HOME_ROOT_DIR, RPI_HOME_WWW_DIR, NAME, VERSION, SENSORS, CONTROLS, TIMESTAMP, HOST, IP_ADDRESS, \
    OPERATING_SYSTEM, DRIVER, CLASS_NAME, DRIVER_DEFAULT_CLASS_NAME
from .utils import get_lines_from_proc, load_json_file, put_if_not_none
from .rpi_sensor import RpiSensor
from .driver import install_driver

_LOGGER = logging.getLogger(__name__)


def _get_ip_address() -> str:
    for line in get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
        if 'eth0' in line or 'wlan0' in line:
            return line.split()[3].split("/")[0]
    # if we didn't get anything else...
    return socket.gethostbyname(socket.gethostname())


def _get_os_description() -> str:
    for line in get_lines_from_proc(["lsb_release", "-a"]):
        if "Description" in line:
            return line.split(':')[1].strip()
    # if we didn't get anything else
    return "unknown"


class RpiSensorDevice:
    def __init__(self):
        # set up the driver cache
        self.driver_cache: dict[str, RpiSensor] = {}

        # load the config
        config_file = os.path.join(RPI_HOME_ROOT_DIR, "config.json")
        self._config = load_json_file(config_file)
        assert self.config is not None

        # run through the config and try to install each module, then cache the driver
        sensors = self._config[SENSORS]
        for sensor in sensors:
            # sensor has a driver (a pip module dependency), and an optional "class_name" with a default of "Driver"
            driver = sensor[DRIVER]
            class_name = self.driver_class_name(sensor)
            cache_name = self.driver_cache_name(driver, class_name)
            put_if_not_none(self.driver_cache, cache_name, install_driver(driver, class_name))

    @staticmethod
    def driver_class_name(sensor: dict[str, Any]) -> str:
        return sensor.get(CLASS_NAME, DRIVER_DEFAULT_CLASS_NAME)

    @staticmethod
    def driver_cache_name(driver: str, class_name: str) -> str:
        return driver + "-" + class_name

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    @property
    def version(self) -> str:
        return RPI_HOME_VERSION

    def report(self) -> dict:
        output_sensors = []
        output = {
            VERSION: RPI_HOME_VERSION,
            TIMESTAMP: int(time.time() * 1000),
            HOST: {
                NAME: socket.gethostname(),
                IP_ADDRESS: _get_ip_address(),
                OPERATING_SYSTEM: _get_os_description()
            },
            SENSORS: output_sensors
        }

        # load the control states and include them (if any)
        put_if_not_none(output, CONTROLS, load_json_file(os.path.join(RPI_HOME_WWW_DIR, "controls.json")))

        # loop through the config to read each sensor
        sensors = self._config[SENSORS]
        for sensor in sensors:
            # find the driver in the cache
            driver = sensor[DRIVER]
            _LOGGER.debug(f"reading from driver ({driver})")
            cache_name = self.driver_cache_name(driver, self.driver_class_name(sensor))
            if cache_name in self.driver_cache:
                sensor_outputs = self.driver_cache[cache_name].report()
                if sensor_outputs is not None:
                    output_sensors.extend(sensor_outputs)

        return output
