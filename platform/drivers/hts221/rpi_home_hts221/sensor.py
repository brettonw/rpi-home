# see - https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython
import board
from adafruit_hts221 import HTS221
from typing import Any

from ha_tiny import SensorDeviceClass
from rpi_home import RpiHomeSensor, RpiHomeSensorDriver
from .version import DRIVER_VERSION
from .const import (PT, PT100, PT1000, DEFAULT_PT, WIRES, DEFAULT_WIRES, SELECT_PIN,
                    DEFAULT_SELECT_PIN, REF_RESISTOR, RTD_NOMINAL, RESISTANCE,
                    UnitOfResistance)


class Sensor(RpiHomeSensor):
    @classmethod
    def report(cls, driver: RpiHomeSensorDriver) -> list[dict[str, Any]] | None:
        # always on i2c @ 0x5F.
        sensor = HTS221 (board.I2C())
        return [
            driver.make_float_sensor(None, None, sensor.temperature, 3, SensorDeviceClass.TEMPERATURE),
            driver.make_float_sensor(None, None, sensor.relative_humidity, 3, SensorDeviceClass.HUMIDITY),
        ]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
