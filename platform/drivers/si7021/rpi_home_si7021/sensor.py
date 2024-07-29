from typing import Any

from adafruit_si7021 import SI7021
import board
from homeassistant.components.sensor import SensorDeviceClass
from rpi_home import RpiHomeSensor, RpiHomeSensorBuilder
from .version import DRIVER_VERSION

class Sensor(RpiHomeSensor):
    @classmethod
    def report(cls) -> list[dict[str, Any]] | None:
        sensor = SI7021 (board.I2C())
        return [
            RpiHomeSensorBuilder.make_float_sensor("temperature", sensor.temperature, 2, SensorDeviceClass.TEMPERATURE),
            RpiHomeSensorBuilder.make_float_sensor("humidity", sensor.relative_humidity, 2, SensorDeviceClass.HUMIDITY)
        ]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
