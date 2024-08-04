from __future__ import annotations

import inspect
from typing import Any

from homeassistant.const import PERCENTAGE
from homeassistant.components.sensor import SensorDeviceClass

from rpi_home import RpiHomeSensor, RpiHomeSensorBuilder, get_fields_from_proc, get_float_field_from_proc
from .version import DRIVER_VERSION


class Sensor(RpiHomeSensor):
    @classmethod
    def uptime(cls):
        uptime = get_float_field_from_proc(["cat", "/proc/uptime"], 0, 0)
        return RpiHomeSensorBuilder.make_float_sensor("Uptime", inspect.currentframe().f_code.co_name, uptime, 2, SensorDeviceClass.DURATION)

    @classmethod
    def cpu_usage(cls) -> dict:
        usage = 100.0 - get_float_field_from_proc("mpstat", -1, -1)
        return RpiHomeSensorBuilder.make_float_sensor("CPU Usage", inspect.currentframe().f_code.co_name, usage, 2, PERCENTAGE)

    @classmethod
    def cpu_temperature(cls) -> dict:
        temperature = get_float_field_from_proc(["cat", "/sys/class/thermal/thermal_zone0/temp"], 0, 0) / 1000.0
        return RpiHomeSensorBuilder.make_float_sensor("CPU Temperature", inspect.currentframe().f_code.co_name, temperature, 3, SensorDeviceClass.TEMPERATURE)

    @classmethod
    def memory_usage(cls):
        fields = get_fields_from_proc(["free", "-bw"], 1)
        total = float(fields[1])
        return RpiHomeSensorBuilder.make_float_sensor("Memory Usage", inspect.currentframe().f_code.co_name, (100.0 * (total - float(fields[-1]))) / total, 2, PERCENTAGE)

    @classmethod
    def swap_usage(cls):
        fields = get_fields_from_proc(["free", "-bw"], 2)
        return RpiHomeSensorBuilder.make_float_sensor("Swap Usage", inspect.currentframe().f_code.co_name, (100.0 * float(fields[2])) / float(fields[1]), 2, PERCENTAGE)

    @classmethod
    def disk_usage(cls):
        fields = get_fields_from_proc(["df", "--block-size=1K", "--output=size,used,avail", "/"], 1)
        return RpiHomeSensorBuilder.make_float_sensor("Disk Usage", inspect.currentframe().f_code.co_name, (100.0 * float(fields[1])) / float(fields[0]), 2, PERCENTAGE)

    @classmethod
    def report(cls) -> list[dict[str, Any]] | None:
        return [cls.uptime(), cls.cpu_usage(), cls.cpu_temperature(), cls.memory_usage(), cls.swap_usage(), cls.disk_usage()]

    @classmethod
    def version(cls) -> str:
        return DRIVER_VERSION
