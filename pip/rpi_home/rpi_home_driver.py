import logging
import subprocess
import sys
import os
import re
import importlib
from typing import Any, Type, TypeVar

from homeassistant.const import UnitOfTime, UnitOfTemperature, UnitOfInformation
from homeassistant.components.sensor import SensorDeviceClass, DEVICE_CLASS_UNITS

from .const import (RPI_HOME_ROOT_DIR, DRIVER_PREFIX, DRIVER, CLASS_NAME, DISPLAY_NAME, VALUE,
                    VALUES, SENSOR_DEVICE_CLASS, UNIT_OF_MEASUREMENT, ENTITY_ID, REMAP)
from .rpi_home_entity import RpiHomeEntity, RpiHomeSensor, RpiHomeControl
from .utils import put_if_not_none

logger = logging.getLogger(__name__)


# Define a type variable constrained to RpiEntity or its subclasses
EntityType = TypeVar("EntityType", bound=RpiHomeEntity)


# helper function to install a module and look up a class
def _install_driver(driver: str, class_name: str, required_type: Type[EntityType]) -> EntityType | None:
    # condition the module name to start with "rpi_home_"
    if driver.startswith(DRIVER_PREFIX):
        driver = driver[len(DRIVER_PREFIX):]

    # use pip to install or upgrade the module
    try:
        # XXX can we find the drivers path instead of hardcode it?
        module_path = os.path.join(RPI_HOME_ROOT_DIR, "platform", "drivers", driver)
        logger.debug(f"installing driver ({driver})")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module_path])
        logger.debug(f"  installed driver ({driver})")
    except subprocess.CalledProcessError as e:
        logger.error(f"failed to install or upgrade module for driver ({driver}): {e}")

    # condition the module name to start with "rpi_home_"
    driver = DRIVER_PREFIX + driver

    # try to load the module
    try:
        imported_module = importlib.import_module(driver)
    except ModuleNotFoundError:
        logger.error(f"module ({driver}) not found.")
        return None

    # try to get the requested class
    try:
        imported_class = getattr(imported_module, class_name)
    except AttributeError:
        logger.error(f"class ({class_name}) not found in module '{driver}'.")
        return None

    # ensure that the found attribute is a subclass of the required type
    if not issubclass(imported_class, required_type):
        logger.error(f"class ({class_name}) in module ({driver}) is not a subclass of {required_type}")
        return None

    return imported_class


class RpiHomeDriverName:
    def __init__(self, entity: dict[str, Any], required_type: Type[EntityType]):
        self._module_name = entity[DRIVER]
        self._class_name = entity.get(CLASS_NAME, required_type.get_default_class_name())
        self._cache_name = self._module_name + "-" + self._class_name
        # XXX validate the remap?
        self._remap = entity.get(REMAP, {DISPLAY_NAME: {}, ENTITY_ID: {}})

    @property
    def module_name(self) -> str:
        return self._module_name

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def cache_name(self) -> str:
        return self._cache_name


class RpiHomeDriver(RpiHomeDriverName):
    def __init__(self, entity: dict[str, Any], required_type: Type[EntityType]):
        super().__init__(entity, required_type)
        self.cls = _install_driver(self.module_name, self.class_name, required_type)

    @property
    def is_valid(self) -> bool:
        return self.cls is not None


class RpiHomeSensorDriver(RpiHomeDriver):
    _SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT = {
        SensorDeviceClass.DURATION: UnitOfTime.SECONDS,
        SensorDeviceClass.TEMPERATURE: UnitOfTemperature.CELSIUS,
        SensorDeviceClass.DATA_SIZE: UnitOfInformation.BYTES
    }

    def _verify_unit(self, sensor_device_class: SensorDeviceClass | str, unit: str | None) -> str | None:
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
                    if sensor_device_class in self._SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT:
                        return self._SENSOR_DEVICE_CLASS_DEFAULT_UNIT_OF_MEASUREMENT[sensor_device_class]

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

    def _make_sensor(self, record: dict, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        record[SENSOR_DEVICE_CLASS] = sensor_device_class
        put_if_not_none(record, UNIT_OF_MEASUREMENT, self._verify_unit(sensor_device_class, unit_of_measurement))
        return record

    def display_name_and_or_entity_id(self, display_name: str | None, entity_id: str | None) -> dict[str, Any]:
        # one of them must be non-None
        assert (entity_id is not None) or (display_name is not None)

        # if entity_id is empty, we make up one from the display name, similarly for the display name
        if entity_id is None:
            entity_id = re.sub(r"[^A-Za-z_]", "", re.sub(r"[- ]", "_", display_name.lower()))
        if display_name is None:
            display_name = entity_id.replace("_", " ").title()

        # make a record with both values, remapped as necessary, and return it
        return {
            DISPLAY_NAME: self._remap.get(DISPLAY_NAME, {}).get(display_name, display_name),
            ENTITY_ID: self._remap.get(ENTITY_ID, {}).get(entity_id, entity_id)
        }

    def make_float_value(self, display_name: str | None, entity_id: str | None, value: float, precision: int) -> dict:
        record = self.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUE] = round(value, precision)
        return record

    def make_int_value(self, display_name: str | None, entity_id: str | None, value: int) -> dict:
        record = self.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUE] = value
        return record

    def make_float_sensor(self, display_name: str | None, entity_id: str | None, value: float, precision: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return self._make_sensor(self.make_float_value(display_name, entity_id, value, precision), sensor_device_class, unit_of_measurement)

    def make_int_sensor(self, display_name: str | None, entity_id: str | None, value: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return self._make_sensor(self.make_int_value(display_name, entity_id, value), sensor_device_class, unit_of_measurement)

    def make_group_sensor(self, display_name: str | None, entity_id: str | None, values: list[dict[str, Any]], sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        record = self.display_name_and_or_entity_id(display_name, entity_id)
        record[VALUES] = values
        return self._make_sensor(record, sensor_device_class, unit_of_measurement)

    def __init__(self, entity: dict[str, Any]):
        super().__init__(entity, RpiHomeSensor)

    def report(self) -> list[dict[str, Any]] | None:
        # XXX maybe in the future this should be an object, not a class - then it could maintain a history, etc.
        return self.cls.report(self)


class RpiHomeControlDriver(RpiHomeDriver):
    def __init__(self, entity: dict[str, Any]):
        super().__init__(entity, RpiHomeControl)

    def report(self) -> list[dict[str, Any]] | None:
        # XXX maybe in the future this should be an object, not a class - then it could maintain a history, etc.
        return self.cls.perform(self)
