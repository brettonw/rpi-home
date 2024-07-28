from __future__ import annotations

import logging

from homeassistant.const import UnitOfTime, UnitOfTemperature, UnitOfInformation
from homeassistant.components.sensor import SensorDeviceClass, DEVICE_CLASS_UNITS

from .const import NAME, VALUE, VALUES, UNIT_OF_MEASUREMENT
from .utils import put_if_not_none

_LOGGER = logging.getLogger(__name__)


class RpiSensorBuilder:
    _SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT = {
        SensorDeviceClass.DURATION: UnitOfTime.SECONDS,
        SensorDeviceClass.TEMPERATURE: UnitOfTemperature.CELSIUS,
        SensorDeviceClass.DATA_SIZE: UnitOfInformation.BYTES
    }

    @classmethod
    def _verify_unit(cls, sensor_device_class: SensorDeviceClass | str, unit: str | None) -> str | None:
        # check to see if the sensor_device_class is in the sensor_device_class->unit mapping, and if so, either
        # validate the unit passed, or return a default (if possible)
        if sensor_device_class in DEVICE_CLASS_UNITS:
            units = DEVICE_CLASS_UNITS[sensor_device_class]
            if len(units) > 0:
                if unit is None:
                    # if there is only one unit for the device class, assume that's the default
                    if len(units) == 1:
                        return next(iter(units))

                    # if we have a default, use that
                    if sensor_device_class in cls._SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT:
                        return cls._SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT[sensor_device_class]

                    # we're out of ideas... return the first unit in the list
                    # XXX could warn the user the choice is apparently random if units has more than one
                    # XXX entry
                    return next(iter(units))

                # if we passed a unit, then check it's in the list
                if unit in units:
                    return unit
                else:
                    # XXX could warn the user their choice appears to be incorrect
                    return unit

        # we don't know what this is
        return unit

    @classmethod
    def _make_sensor(cls, record: dict, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        record["sensor_device_class"] = sensor_device_class
        put_if_not_none(record, UNIT_OF_MEASUREMENT, cls._verify_unit(sensor_device_class, unit_of_measurement))
        return record

    @classmethod
    def make_float_value(cls, name: str, value: float, precision: int) -> dict:
        return {NAME: name, VALUE: round(value, precision)}

    @classmethod
    def make_int_value(cls, name: str, value: float) -> dict:
        return {NAME: name, VALUE: value}

    @classmethod
    def make_float_sensor(cls, name: str, value: float, precision: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_float_value(name, value, precision), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_int_sensor(cls, name: str, value: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_int_value(name, value), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_group_sensor(cls, name: str, values: list[dict], sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor({NAME: name, VALUES: values}, sensor_device_class, unit_of_measurement)
