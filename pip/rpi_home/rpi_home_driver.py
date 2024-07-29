import logging
import subprocess
import sys
import os
import importlib
from typing import Any, Type, TypeVar

from .const import (RPI_HOME_ROOT_DIR, DRIVER_PREFIX, DRIVER, CLASS_NAME)
from .rpi_home_entity import RpiHomeEntity, RpiHomeSensor, RpiHomeControl

_LOGGER = logging.getLogger(__name__)


# Define a type variable constrained to RpiEntity or its subclasses
EntityType = TypeVar("EntityType", bound=RpiHomeEntity)


# helper function to install a module and look up a class
def _install_driver(driver: str, class_name: str, required_type: Type[EntityType]) -> EntityType | None:
    # condition the module name to start with "rpi_home_"
    if driver.startswith(DRIVER_PREFIX):
        driver = driver[len(DRIVER_PREFIX):]

    # use pip to install or upgrade the module
    try:
        module_path = os.path.join(RPI_HOME_ROOT_DIR, "rpi", "drivers", driver)
        _LOGGER.debug(f"installing driver ({driver})")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', module_path])
        _LOGGER.debug(f"  installed driver ({driver})")
    except subprocess.CalledProcessError as e:
        _LOGGER.error(f"failed to install or upgrade module for driver ({driver}): {e}")

    # condition the module name to start with "rpi_home_"
    driver = DRIVER_PREFIX + driver

    # try to load the module
    try:
        imported_module = importlib.import_module(driver)
    except ModuleNotFoundError:
        _LOGGER.error(f"module ({driver}) not found.")
        return None

    # try to get the requested class
    try:
        imported_class = getattr(imported_module, class_name)
    except AttributeError:
        _LOGGER.error(f"class ({class_name}) not found in module '{driver}'.")
        return None

    # ensure that the found attribute is a subclass of the required type
    if not issubclass(imported_class, required_type):
        _LOGGER.error(f"class ({class_name}) in module ({driver}) is not a subclass of {required_type}")
        return None

    return imported_class


class RpiHomeDriverName:
    def __init__(self, entity: dict[str, Any], required_type: Type[EntityType]):
        self._module_name = entity[DRIVER]
        self._class_name = entity.get(CLASS_NAME, required_type.get_default_class_name())
        self._cache_name = self._module_name + "-" + self._class_name

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
    def __init__(self, entity: dict[str, Any]):
        super().__init__(entity, RpiHomeSensor)

    def report(self) -> list[dict[str, Any]] | None:
        # XXX maybe in the future this should be an object, not a class - then it could maintain a history, etc.
        return self.cls.report()


class RpiHomeControlDriver(RpiHomeDriver):
    def __init__(self, entity: dict[str, Any]):
        super().__init__(entity, RpiHomeControl)

    def report(self) -> list[dict[str, Any]] | None:
        # XXX maybe in the future this should be an object, not a class - then it could maintain a history, etc.
        return self.cls.perform()
