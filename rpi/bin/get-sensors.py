#! /usr/local/rpi_home/python3/bin/python3

from rpi_sensor import RpiSensorDevice
import json

if __name__ == "__main__":
    sensor_logger = RpiSensorDevice()
    print(json.dumps(sensor_logger.report()))
