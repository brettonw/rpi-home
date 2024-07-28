#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import os
import sys
import time
import socket

from homeassistant.const import UnitOfTime, UnitOfTemperature, UnitOfInformation, PERCENTAGE
from homeassistant.components.sensor import SensorDeviceClass, DEVICE_CLASS_UNITS

VERSION = "2.0.0"


def _check_type_unit(sensor_device_class: SensorDeviceClass | str, unit: str | None) -> str | None:
    # check to see if the sensor_device_class is in the sensor_device_class->unit mapping, and if so, either
    # validate the unit passed, or return a default (if possible)
    if sensor_device_class in DEVICE_CLASS_UNITS:
        units = DEVICE_CLASS_UNITS[sensor_device_class]
        if len(units) > 0:
            if unit is None:
                # just return the first one, assuming it's a default
                # XXX could warn the user the choice is apparently random if units has more than one
                # XXX entry
                return next(iter(units))

            if unit in units:
                return unit
            else:
                # XXX could warn the user their choice appears to be incorrect
                return unit

    # we don't know what this is
    return unit


def _make_float_sensor(name: str, value: float, precision: int, sensor_device_class: SensorDeviceClass | str, unit: str | None = None) -> dict:
    return {"name": name, "value": round(value, precision), "sensor_device_class": sensor_device_class, "unit": _check_type_unit(sensor_device_class, unit)}


def _make_int_sensor(name: str, value: int, sensor_device_class: SensorDeviceClass | str, unit: str | None = None) -> dict:
    return {"name": name, "value": value, "sensor_device_class": sensor_device_class, "unit": _check_type_unit(sensor_device_class, unit)}


# utility functions to get infor from the host
def _get_ip_address():
    source =
    result = subprocess.run(['ip', '-o', '-4', 'addr', 'list'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'eth0' in line or 'wlan0' in line:
            return line.split()[3].split('/')[0]
    return ""


def _get_os_description():
    result = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Description' in line:
            return line.split(':')[1].strip()
    return ""


def _get_uptime():
    with open('/proc/uptime', 'r') as f:
        return _make_float_sensor('uptime', float(f.readline().split()[0]), 3, SensorDeviceClass.DURATION, UnitOfTime.SECONDS)


def _get_cpu_load():
    result = subprocess.run(['mpstat'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    last_line = lines[-2]
    fields = last_line.split()
    return (_SensorGroup("cpu_load", PERCENTAGE)
            .add_float_sensor("usr", float(fields[2]), 2)
            .add_float_sensor("sys", float(fields[4]), 2)
            .add_float_sensor("idle", float(fields[-1]), 2)
            .add_float_sensor("percent", 100.0 - float(fields[-1]), 2)
            .finish()
            )


def _get_cpu_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = f.read().strip()
        return _make_float_sensor("cpu_temperature", float(temp) / 1000.0, 3, SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS)


def _get_memory():
    result = subprocess.run(['free', '-bw'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    memory_line = lines[1]
    fields = memory_line.split()
    total = int(fields[2])
    available = int(fields[-1])
    return (_SensorGroup("memory", SensorDeviceClass.DATA_SIZE, UnitOfInformation.BYTES)
            .add_int_sensor("total", total)
            .add_int_sensor("used", int(fields[4]))
            .add_int_sensor("free", int(fields[-1]))
            .add_int_sensor("shared", int(fields[-1]))
            .add_int_sensor("buffers", int(fields[-1]))
            .add_int_sensor("cache", int(fields[-1]))
            .add_int_sensor("available", available)
            .add_float_sensor("percent", (100.0 * (total - available)) / total, 2)
            .finish()
            )


def _get_swap():
    result = subprocess.run(['free', '-bw'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    swap_line = lines[2]
    fields = swap_line.split()
    total = int(fields[1])
    used = int(fields[2])
    return (_SensorGroup("swap", SensorDeviceClass.DATA_SIZE, UnitOfInformation.BYTES)
            .add_int_sensor("total", total)
            .add_int_sensor("used", used)
            .add_int_sensor("free", int(fields[3]))
            .add_float_sensor("percent", (100.0 * used) / total, 2)
            .finish()
            )


def _get_disk():
    result = subprocess.run(['df', '--block-size=1K', '--output=size,used,avail', '/'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    disk_line = lines[1]
    fields = disk_line.split()
    total = int(fields[0])
    used = int(fields[1])
    return (_SensorGroup("disk", SensorDeviceClass.DATA_SIZE, UnitOfInformation.BYTES)
            .add_int_sensor("total", total)
            .add_int_sensor("used", used)
            .add_int_sensor("free", int(fields[2]))
            .add_float_sensor("percent", (100.0 * used) / total, 2)
            .finish()
            )


class SensorLogger:
    def __init__(self):
        self.sensor_dir = "/var/www/html/sensor"
        with open(os.path.join(self.sensor_dir, "config.json"), 'r') as config_file:
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

    def log_sensor_data(self):
        timestamp = int(time.time() * 1000)
        hostname = socket.gethostname()

        output = {
            "version": VERSION,
            "timestamp": timestamp,
            "host": {
                "name": hostname,
                "ip": socket.gethostbyname(hostname),
                "os": _get_os_description()
            },
            "sensors": [_get_uptime(), _get_cpu_load(), _get_cpu_temperature(), _get_memory(), _get_swap(), _get_disk()]
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

        now_file = os.path.join(self.sensor_dir, "nowx.json")
        with open(now_file, 'w') as f:
            json.dump(output, f)

        self.counter += 1
        interval = 15000
        target_timestamp = self.start_timestamp + (self.counter * interval)
        now_timestamp = int(time.time() * 1000)
        delta = (target_timestamp - now_timestamp) / 1000
        if delta > 0:
            time.sleep(delta)
        else:
            self._echoerr(f"PROBLEM: not sleeping ({delta * 1000} ms)")


if __name__ == "__main__":
    sensor_logger = SensorLogger()
    # while True:
    #     sensor_logger.log_sensor_data()
    sensor_logger.log_sensor_data()
