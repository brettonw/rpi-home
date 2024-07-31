from __future__ import annotations

import os
import socket
import logging
from typing import Any

from .version import RPI_HOME_VERSION
from .const import RPI_HOME_ROOT_DIR, NAME, VERSION, SENSORS, CONTROLS, SETTINGS, TIMESTAMP, HOST, IP_ADDRESS, OPERATING_SYSTEM
from .utils import get_lines_from_proc, load_json_file, timestamp, get_ip_address
from .rpi_home_driver import RpiHomeSensorDriver, RpiHomeControlDriver

_LOGGER = logging.getLogger(__name__)


class RpiHomeDevice:
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
        self.ip_address = get_ip_address()
        self.os_description = self._get_os_description()

        # run through the config and cache the sensor drivers
        self._sensors: list[RpiHomeSensorDriver] = []
        for sensor in self._config[SENSORS]:
            driver = RpiHomeSensorDriver(sensor)
            if driver.is_valid:
                self._sensors.append(driver)

        # run through the config and cache the control drivers
        self._controls: list[RpiHomeControlDriver] = []
        for control in self._config[CONTROLS]:
            driver = RpiHomeControlDriver(control)
            if driver.is_valid:
                self._controls.append(driver)

    @property
    def settings(self) -> dict[str, Any]:
        return self._config[SETTINGS]

    @property
    def sensors(self) -> list[RpiHomeSensorDriver]:
        return self._sensors

    @property
    def controls(self) -> list[RpiHomeControlDriver]:
        return self._controls

    @property
    def version(self) -> str:
        return RPI_HOME_VERSION

    @property
    def sampling_interval(self) -> float:
        return float(self.settings["sampling_interval"])

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
            _LOGGER.debug(f"reading from driver ({sensor.cache_name})")
            sensor_report = sensor.report()
            if sensor_report is not None:
                output_sensors.extend(sensor_report)

        return output
