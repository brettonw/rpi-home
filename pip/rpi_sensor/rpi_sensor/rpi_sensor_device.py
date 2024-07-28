from __future__ import annotations

import json
import subprocess
import os
import time
import socket
import logging

from .version import RPI_HOME_VERSION
from .const import RPI_SENSOR_DIR, NAME, VERSION, SENSORS, CONTROLS, TIMESTAMP, HOST, IP_ADDRESS, OPERATING_SYSTEM
from .utils import get_lines_from_proc, load_json_file, put_if_not_none
from .rpi_sensor_host import RpiSensorHost

_LOGGER = logging.getLogger(__name__)


def _get_ip_address() -> str:
    for line in get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
        if 'eth0' in line or 'wlan0' in line:
            return line.split()[3].split("/")[0]
    # if we didn't get anything else...
    return socket.gethostbyname(socket.gethostname())


def _get_os_description() -> str:
    for line in get_lines_from_proc(["lsb_release", "-a"]):
        if "Description" in line:
            return line.split(':')[1].strip()
    # if we didn't get anything else
    return "unknown"


class RpiSensorDevice:
    def __init__(self):
        config_file = os.path.join(RPI_SENSOR_DIR, "config.json")
        if os.path.isfile(config_file):
            with open(config_file, 'r') as config_file:
                self.config = json.load(config_file)

    @staticmethod
    def _read_sensor():
        result = subprocess.run(['/home/brettonw/bin/sensor.py'], capture_output=True, text=True)
        return json.loads(result.stdout.strip())

    def report(self) -> dict:
        output = {
            VERSION: RPI_HOME_VERSION,
            TIMESTAMP: int(time.time() * 1000),
            HOST: {
                NAME: socket.gethostname(),
                IP_ADDRESS: _get_ip_address(),
                OPERATING_SYSTEM: _get_os_description()
            },
            SENSORS: RpiSensorHost.report()
        }

        # load the control states and include them (if any)
        put_if_not_none(output, CONTROLS, load_json_file(os.path.join(RPI_SENSOR_DIR, "controls.json")))

        # loop through the config to read each sensor
        # sensor_read = self._read_sensor()
        # if sensor_read:
        #     output["sensors"]["sensors"].append(sensor_read)

        return output
