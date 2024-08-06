from __future__ import annotations

import inspect
from typing import Any

from ha_tiny import PERCENTAGE, SensorDeviceClass
from rpi_home import RpiHomeSensor, RpiHomeSensorDriver, get_fields_from_proc, get_float_field_from_proc
from .version import DRIVER_VERSION


def uptime(driver: RpiHomeSensorDriver):
    value = get_float_field_from_proc(["cat", "/proc/uptime"], 0, 0)
    return driver.make_float_sensor(None, inspect.currentframe().f_code.co_name, value, 2, SensorDeviceClass.DURATION)


def cpu_usage(driver: RpiHomeSensorDriver) -> dict:
    value = 100.0 - get_float_field_from_proc("mpstat", -1, -1)
    return driver.make_float_sensor("CPU Usage", inspect.currentframe().f_code.co_name, value, 2, PERCENTAGE)


def cpu_temperature(driver: RpiHomeSensorDriver) -> dict:
    value = get_float_field_from_proc(["cat", "/sys/class/thermal/thermal_zone0/temp"], 0, 0) / 1000.0
    return driver.make_float_sensor("CPU Temperature", inspect.currentframe().f_code.co_name, value, 3, SensorDeviceClass.TEMPERATURE)


def memory_usage(driver: RpiHomeSensorDriver):
    fields = get_fields_from_proc(["free", "-bw"], 1)
    total = float(fields[1])
    return driver.make_float_sensor(None, inspect.currentframe().f_code.co_name, (100.0 * (total - float(fields[-1]))) / total, 2, PERCENTAGE)


def swap_usage(driver: RpiHomeSensorDriver):
    fields = get_fields_from_proc(["free", "-bw"], 2)
    return driver.make_float_sensor(None, inspect.currentframe().f_code.co_name, (100.0 * float(fields[2])) / float(fields[1]), 2, PERCENTAGE)


def disk_usage(driver: RpiHomeSensorDriver):
    fields = get_fields_from_proc(["df", "--block-size=1K", "--output=size,used,avail", "/"], 1)
    return driver.make_float_sensor(None, inspect.currentframe().f_code.co_name, (100.0 * float(fields[1])) / float(fields[0]), 2, PERCENTAGE)


class Sensor(RpiHomeSensor):
    @classmethod
    def report(cls, driver: RpiHomeSensorDriver) -> list[dict[str, Any]] | None:
        return [uptime(driver), cpu_usage(driver), cpu_temperature(driver), memory_usage(driver), swap_usage(driver), disk_usage(driver)]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
