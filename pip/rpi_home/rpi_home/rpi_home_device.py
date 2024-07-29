from __future__ import annotations

import os
import socket
import logging
from typing import Any, cast

from .version import RPI_HOME_VERSION
from .const import RPI_HOME_ROOT_DIR, NAME, VERSION, SENSORS, CONTROLS, SETTINGS, TIMESTAMP, HOST, \
    IP_ADDRESS, OPERATING_SYSTEM, CACHE
from .utils import get_lines_from_proc, load_json_file, timestamp
from .rpi_home_driver import RpiHomeSensorDriver, RpiHomeControlDriver

_LOGGER = logging.getLogger(__name__)


class RpiHomeDevice:
    @staticmethod
    def _get_ip_address() -> str:
        for line in get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
            if 'eth0' in line or 'wlan0' in line:
                return line.split()[3].split("/")[0]
        # if we didn't get anything else...
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def _get_os_description() -> str:
        for line in get_lines_from_proc(["lsb_release", "-a"]):
            if "Description" in line:
                return line.split(':')[1].strip()
        # if we didn't get anything else
        return "unknown"

    @staticmethod
    def driver_cache_name(driver: str, class_name: str) -> str:
        return driver + "-" + class_name

    def __init__(self):
        # load the config
        config_file = os.path.join(RPI_HOME_ROOT_DIR, "config.json")
        self._config = load_json_file(config_file)
        assert self._config is not None

        # store off a few static values
        self.hostname = socket.gethostname()
        self.ip_address = self._get_ip_address()
        self.os_description = self._get_os_description()

        # run through the config and try to cache the drivers
        for sensor in self.sensors:
            driver = RpiHomeSensorDriver(sensor)
            if driver.is_valid:
                sensor[CACHE] = driver
        for control in self.controls:
            driver = RpiHomeControlDriver(control)
            if driver.is_valid:
                control[CACHE] = driver

    @property
    def settings(self) -> dict[str, Any]:
        return self._config[SETTINGS]

    @property
    def controls(self) -> list[dict[str, Any]]:
        return self._config[CONTROLS]

    @property
    def sensors(self) -> list[dict[str, Any]]:
        return self._config[SENSORS]

    @property
    def version(self) -> str:
        return RPI_HOME_VERSION

    def report(self) -> dict:
        output_sensors = []
        output = {
            VERSION: RPI_HOME_VERSION,
            TIMESTAMP: timestamp(),
            HOST: {
                NAME: self.hostname,
                IP_ADDRESS: self.ip_address,
                OPERATING_SYSTEM: self.os_description
            },
            SENSORS: output_sensors
        }

        # load the control states and include them (if any)
        # put_if_not_none(output, CONTROLS, load_json_file(os.path.join(RPI_HOME_WWW_DIR, "controls.json")))

        # loop through the config to read each sensor
        for sensor in self.sensors:
            if CACHE in sensor:
                driver = cast(sensor[CACHE], RpiHomeSensorDriver)
                _LOGGER.debug(f"reading from driver ({driver.cache_name})")
                sensor_outputs = driver.report()
                if sensor_outputs is not None:
                    output_sensors.extend(sensor_outputs)

        return output
