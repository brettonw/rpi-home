# see - https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython
import board
import digitalio
import adafruit_max31865
from typing import Any

from ha_tiny import SensorDeviceClass
from rpi_home import RpiHomeSensor, RpiHomeSensorDriver
from .version import DRIVER_VERSION
from .const import (PT, PT100, PT1000, DEFAULT_PT, WIRES, DEFAULT_WIRES, CHIP_SELECT_PIN,
                    DEFAULT_CHIP_SELECT_PIN, REF_RESISTOR, RTD_NOMINAL, RESISTANCE,
                    UnitOfResistance)


class Sensor(RpiHomeSensor):
    pt_params = {
        PT100: {RTD_NOMINAL: 100, REF_RESISTOR: 430},
        PT1000: {RTD_NOMINAL: 1000, REF_RESISTOR: 4300}
    }

    @classmethod
    def report(cls, driver: RpiHomeSensorDriver) -> list[dict[str, Any]] | None:
        # get the parameters from the driver, with defaults... that might not work...
        parameters = driver.parameters
        (wires, pt, chip_select_pin) = (
            int(parameters.get(WIRES, DEFAULT_WIRES)),
            cls.pt_params.get(parameters.get(PT, DEFAULT_PT), cls.pt_params.get(PT100)),
            getattr(board, parameters.get(CHIP_SELECT_PIN, DEFAULT_CHIP_SELECT_PIN), None)
        )

        # instantiate the sensor
        sensor = adafruit_max31865.MAX31865(
            board.SPI(),
            digitalio.DigitalInOut(chip_select_pin),
            wires=wires,
            rtd_nominal=pt[RTD_NOMINAL],
            ref_resistor=pt[REF_RESISTOR]
        )

        #
        return [
            driver.make_float_sensor(None, None, sensor.temperature, 3, SensorDeviceClass.TEMPERATURE),
            # XXX resistance is not a standard sensor device class in home assistant
            driver.make_float_sensor(None, None, sensor.resistance, 3, RESISTANCE, UnitOfResistance.OHM),
        ]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
