from __future__ import annotations

import os
import socket
import logging
from typing import Any

from .version import RPI_HOME_VERSION
from .const import *
from .utils import load_json_file, get_ip_address, get_mac_address, get_serial_number, get_os_description, timestamp
from .rpi_home_driver import RpiHomeSensorDriver, RpiHomeControlDriver

logger = logging.getLogger(__name__)


class RpiHomeDevice:
    @staticmethod
    def driver_cache_name(driver: str, class_name: str) -> str:
        return driver + "-" + class_name

    def __init__(self):
        # load the config
        config_file = os.path.join(RPI_HOME_ROOT_DIR, "config.json")
        self._config = load_json_file(config_file)
        if self._config is None:
            logger.warning(f"using default config. at a minimum, copy the example config")
            self._config = {SETTINGS: {DISPLAY_NAME: "[Change Me]", SAMPLING_INTERVAL: 10}, SENSORS: [{DRIVER: HOST}], CONTROLS: []}

        # store off a few static values
        self._hostname = socket.gethostname()
        self._display_name = self.settings.get(DISPLAY_NAME, self._hostname.capitalize())
        self._ip_address = get_ip_address()
        self._mac_address = get_mac_address()
        self._serial_number = get_serial_number()
        self._os_description = get_os_description()

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

        # XXX do a test to assert unique names?

    @property
    def settings(self) -> dict[str, Any]:
        return self._config.get(SETTINGS, {})

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
        return float(self.settings.get(SAMPLING_INTERVAL, DEFAULT_SAMPLING_INTERVAL))

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def mac_address(self) -> dict[str, str]:
        return self._mac_address

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @property
    def os_description(self) -> str:
        return self._os_description

    def report(self) -> dict:
        output_sensors = []
        output = {
            VERSION: RPI_HOME_VERSION,
            TIMESTAMP: timestamp(),
            HOST: {
                DISPLAY_NAME: self._display_name,
                NAME: self._hostname,
                IP_ADDRESS: self._ip_address,
                MAC_ADDRESS: self._mac_address,
                SERIAL_NUMBER: self._serial_number,
                OPERATING_SYSTEM: self._os_description
            },
            SENSORS: output_sensors
        }

        # load the control states and include them (if any)
        # put_if_not_none(output, CONTROLS, load_json_file(os.path.join(RPI_HOME_WWW_DIR, "controls.json")))

        # loop through the config to read each sensor and check the entity is not in the 'skip' list
        for sensor in self.sensors:
            logger.debug(f"reading from driver ({sensor.cache_name})")
            sensor_reports = sensor.report()
            if sensor_reports is not None:
                for sensor_report in sensor_reports:
                    if sensor_report[ENTITY_ID] not in sensor.skip:
                        logger.debug(f"capturing {sensor_report[ENTITY_ID]}")
                        output_sensors.append(sensor_report)
                    else:
                        logger.debug(f"skipping {sensor_report[ENTITY_ID]}")

        return output
