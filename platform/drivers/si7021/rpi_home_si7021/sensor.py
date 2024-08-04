from typing import Any

from adafruit_si7021 import SI7021
import board
from homeassistant.components.sensor import SensorDeviceClass
from rpi_home import RpiHomeSensor, RpiHomeSensorDriver
from .version import DRIVER_VERSION


class Sensor(RpiHomeSensor):
    @classmethod
    def report(cls, driver: RpiHomeSensorDriver) -> list[dict[str, Any]] | None:
        sensor = SI7021(board.I2C())
        return [
            driver.make_float_sensor(None, "temperature", sensor.temperature, 2, SensorDeviceClass.TEMPERATURE),
            driver.make_float_sensor(None, "humidity", sensor.relative_humidity, 2, SensorDeviceClass.HUMIDITY)
        ]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
