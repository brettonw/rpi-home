from __future__ import annotations

import os
import socket
import logging
from typing import Any

from .version import RPI_HOME_VERSION
from .const import (RPI_HOME_ROOT_DIR, NAME, DISPLAY_NAME, VERSION, SENSORS, CONTROLS, SETTINGS,
                    TIMESTAMP, HOST, IP_ADDRESS, MAC_ADDRESS, OPERATING_SYSTEM, SERIAL_NUMBER,
                    SAMPLING_INTERVAL, DRIVER)
from .utils import (load_json_file, timestamp, get_ip_address, get_mac_address, get_serial_number,
                    get_os_description)
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
            self._config = {SETTINGS: {DISPLAY_NAME: "(Change Me)", SAMPLING_INTERVAL: 10}, SENSORS: [{DRIVER: HOST}],CONTROLS: []}

        # store off a few static values
        # XXX what if the config is busted - we need to validate it somewhere
        self._display_name = self._config[SETTINGS][DISPLAY_NAME]
        self._hostname = socket.gethostname()
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
        return float(self.settings[SAMPLING_INTERVAL])

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

        # loop through the config to read each sensor
        for sensor in self.sensors:
            logger.debug(f"reading from driver ({sensor.cache_name})")
            sensor_report = sensor.report()
            if sensor_report is not None:
                output_sensors.extend(sensor_report)

        return output
