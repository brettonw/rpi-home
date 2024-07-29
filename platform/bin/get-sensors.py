#! /usr/local/rpi_home/python3/bin/python3

from rpi_home import RpiHomeDevice
import json
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    device = RpiHomeDevice()
    print(json.dumps(device.report()))
