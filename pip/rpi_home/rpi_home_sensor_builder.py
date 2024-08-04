from __future__ import annotations

import logging
from typing import Any

from homeassistant.const import UnitOfTime, UnitOfTemperature, UnitOfInformation
from homeassistant.components.sensor import SensorDeviceClass, DEVICE_CLASS_UNITS

from .const import DISPLAY_NAME, VALUE, VALUES, SENSOR_DEVICE_CLASS, UNIT_OF_MEASUREMENT, ENTITY_ID
from .utils import put_if_not_none

logger = logging.getLogger(__name__)


class RpiHomeSensorBuilder:
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
        record[SENSOR_DEVICE_CLASS] = sensor_device_class
        put_if_not_none(record, UNIT_OF_MEASUREMENT, cls._verify_unit(sensor_device_class, unit_of_measurement))
        return record

    @staticmethod
    def display_name_and_or_entity_id(display_name: str | None, entity_id: str | None) -> dict[str, Any]:
        record = {}
        if display_name is not None:
            record[DISPLAY_NAME] = display_name
        if entity_id is not None:
            record[ENTITY_ID] = entity_id
        assert len(record) > 0
        return record

    @classmethod
    def make_float_value(cls, display_name: str, entity_id: str, value: float, precision: int) -> dict:
        record = RpiHomeSensorBuilder.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUE] = round(value, precision)
        return record

    @classmethod
    def make_int_value(cls, display_name: str, entity_id: str, value: int) -> dict:
        record = RpiHomeSensorBuilder.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUE] = value
        return record

    @classmethod
    def make_float_sensor(cls, display_name: str, entity_id: str, value: float, precision: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_float_value(display_name, entity_id, value, precision), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_int_sensor(cls, display_name: str, entity_id: str, value: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_int_value(display_name, entity_id, value), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_group_sensor(cls, display_name: str, entity_id: str, values: list[dict[str, Any]], sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        record = RpiHomeSensorBuilder.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUES] = values
        return cls._make_sensor(record, sensor_device_class, unit_of_measurement)
