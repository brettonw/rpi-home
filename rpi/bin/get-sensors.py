#! /usr/local/rpi_home/python3/bin/python3
from __future__ import annotations

import json
import subprocess
import os
import sys
import time
import socket
import logging

from homeassistant.const import UnitOfTime, UnitOfTemperature, UnitOfInformation, PERCENTAGE
from homeassistant.components.sensor import SensorDeviceClass, DEVICE_CLASS_UNITS

_LOGGER = logging.getLogger(__name__)

VERSION = "2.0.0"


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
        unit_of_measurement = cls._verify_unit(sensor_device_class, unit_of_measurement)
        if unit_of_measurement is not None:
            record["unit_of_measurement"] = unit_of_measurement
        return record

    @classmethod
    def make_float_value(cls, name: str, value: float, precision: int) -> dict:
        return {"name": name, "value": round(value, precision)}

    @classmethod
    def make_int_value(cls, name: str, value: float) -> dict:
        return {"name": name, "value": value}

    @classmethod
    def make_float_sensor(cls, name: str, value: float, precision: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_float_value(name, value, precision), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_int_sensor(cls, name: str, value: int, sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor(cls.make_int_value(name, value), sensor_device_class, unit_of_measurement)

    @classmethod
    def make_group_sensor(cls, name: str, values: list[dict], sensor_device_class: SensorDeviceClass | str, unit_of_measurement: str | None = None) -> dict:
        return cls._make_sensor({"name": name, "values": values}, sensor_device_class, unit_of_measurement)


# utility functions to get info from the host
def _get_lines_from_proc(proc: str | list[str]) -> list[str]:
    source = subprocess.run([proc] if isinstance(proc, str) else proc, capture_output=True, text=True)
    return [line for line in source.stdout.split('\n') if line]


def _get_fields_from_proc(proc: str | list[str], line: int, delimiter: str | None = None) -> list[str]:
    return _get_lines_from_proc(proc)[line].split(delimiter)


def _get_field_from_proc(proc: str | list[str], line: int, field: int, delimiter: str | None = None) -> float:
    return float(_get_fields_from_proc(proc, line, delimiter)[field])


def _get_ip_address() -> str:
    for line in _get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
        if 'eth0' in line or 'wlan0' in line:
            return line.split()[3].split('/')[0]
    # if we didn't get anything else...
    return socket.gethostbyname(socket.gethostname())


def _get_os_description() -> str:
    for line in _get_lines_from_proc(["lsb_release", "-a"]):
        if 'Description' in line:
            return line.split(':')[1].strip()
    # if we didn't get anything else
    return "unknown"


class RpiSensorHost:
    @classmethod
    def uptime(cls):
        uptime = _get_field_from_proc(["cat", "/proc/uptime"], 0, 0)
        return RpiSensorBuilder.make_float_sensor("uptime", uptime, 2, SensorDeviceClass.DURATION)

    @classmethod
    def load(cls) -> dict:
        load = 100.0 - _get_field_from_proc("mpstat", -1, -1)
        return RpiSensorBuilder.make_float_sensor("cpu_load", load, 2, PERCENTAGE)

    @classmethod
    def temperature(cls) -> dict:
        temperature = _get_field_from_proc(["cat", "/sys/class/thermal/thermal_zone0/temp"], 0, 0) / 1000.0
        return RpiSensorBuilder.make_float_sensor("cpu_temperature", temperature, 3, SensorDeviceClass.TEMPERATURE)

    @classmethod
    def memory(cls):
        fields = _get_fields_from_proc(["free", "-bw"], 1)
        total = float(fields[1])
        return RpiSensorBuilder.make_float_sensor("memory", (100.0 * (total - float(fields[-1]))) / total, 2, PERCENTAGE)

    @classmethod
    def swap(cls):
        fields = _get_fields_from_proc(["free", "-bw"], 2)
        return RpiSensorBuilder.make_float_sensor("swap", (100.0 * float(fields[2])) / float(fields[1]), 2, PERCENTAGE)

    @classmethod
    def disk(cls):
        fields = _get_fields_from_proc(["df", "--block-size=1K", "--output=size,used,avail", "/"], 1)
        return RpiSensorBuilder.make_float_sensor("disk", (100.0 * float(fields[1])) / float(fields[0]), 2, PERCENTAGE)

    @classmethod
    def report(cls) -> list[dict]:
        return [cls.uptime(), cls.load(), cls.temperature(), cls.memory(), cls.swap(), cls.disk()]


class RpiSensorDevice:
    def __init__(self):
        self.sensor_dir = "/var/www/html/sensor"
        config_file = os.path.join(self.sensor_dir, "config.json")
        if os.path.isfile(config_file):
            with open(config_file, 'r') as config_file:
                self.config = json.load(config_file)
        self.start_timestamp = int(time.time() * 1000)
        self.counter = 0

    @staticmethod
    def _echoerr(*args):
        print(*args, file=sys.stderr)

    @staticmethod
    def _read_sensor():
        result = subprocess.run(['/home/brettonw/bin/sensor.py'], capture_output=True, text=True)
        return json.loads(result.stdout.strip())

    def report(self):
        output = {
            "version": VERSION,
            "timestamp": int(time.time() * 1000),
            "host": {
                "name": socket.gethostname(),
                "ip": _get_ip_address(),
                "os": _get_os_description()
            },
            "sensors": RpiSensorHost.report()
        }

        # load the control states and append them (if any)
        controls_file = os.path.join(self.sensor_dir, "controls.json")
        if os.path.isfile(controls_file):
            with open(controls_file, 'r') as f:
                controls = json.load(f)
                output["controls"] = controls

        # loop through the config to read each sensor
        # sensor_read = self._read_sensor()
        # if sensor_read:
        #     output["sensors"]["sensors"].append(sensor_read)

        print(json.dumps(output))


if __name__ == "__main__":
    sensor_logger = RpiSensorDevice()
    sensor_logger.report()
