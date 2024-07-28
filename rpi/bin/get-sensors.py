#! /usr/local/rpi_home/python3/bin/python3

from rpi_home import RpiSensorDevice
import json
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    sensor_device = RpiSensorDevice()
    print(json.dumps(sensor_device.report()))
