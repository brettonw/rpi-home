from abc import ABC, abstractmethod
from typing import Any

from .rpi_home_driver import RpiHomeSensorDriver, RpiHomeControlDriver
from .const import DRIVER_DEFAULT_SENSOR_CLASS_NAME, DRIVER_DEFAULT_CONTROL_CLASS_NAME


class RpiHomeEntity(ABC):
    @classmethod
    @abstractmethod
    def version(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_default_class_name(cls) -> str:
        pass


class RpiHomeSensor(RpiHomeEntity):
    @classmethod
    @abstractmethod
    def report(cls, driver: RpiHomeSensorDriver) -> list[dict[str, Any]] | None:
        pass

    @classmethod
    def get_default_class_name(cls) -> str:
        return DRIVER_DEFAULT_SENSOR_CLASS_NAME


class RpiHomeControl(RpiHomeEntity):
    @classmethod
    @abstractmethod
    def perform(cls, data: dict[str, Any], driver: RpiHomeControlDriver) -> bool:
        pass

    @classmethod
    def get_default_class_name(cls) -> str:
        return DRIVER_DEFAULT_CONTROL_CLASS_NAME
