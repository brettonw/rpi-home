from typing import Any

from adafruit_si7021 import SI7021
import board
from statistics import mean, stdev
from time import sleep
from homeassistant.components.sensor import SensorDeviceClass
from rpi_home import RpiSensor, RpiSensorBuilder

class Driver(RpiSensor):
    @classmethod
    def report(cls) -> list[dict[str, Any]] | None:
        sensor = SI7021 (board.I2C())
        return [
            RpiSensorBuilder.make_float_sensor("temperature", sensor.temperature, 2, SensorDeviceClass.TEMPERATURE),
            RpiSensorBuilder.make_float_sensor("humidity", sensor.relative_humidity, 2, SensorDeviceClass.HUMIDITY)
        ]
