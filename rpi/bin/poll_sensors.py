#!/usr/local/rpi_home/python3/bin/python3

import json
import logging
import os
import time

from rpi_home import RpiSensorDevice, RPI_HOME_DIR

_LOGGER = logging.getLogger(__name__)


class SensorService:
    def __init__(self):
        self.rpi_sensor_device = RpiSensorDevice()
        self.start_timestamp = int(time.time() * 1000)
        self.counter = 0

    def poll(self):
        now_file = os.path.join(RPI_HOME_DIR, "nowx.json")
        with open(now_file, 'w') as f:
            json.dump(self.rpi_sensor_device.report(), f)

        self.counter += 1
        config = self.rpi_sensor_device.config
        interval = int(config["settings"]["polling_interval"]) * 1000
        target_timestamp = self.start_timestamp + (self.counter * interval)
        now_timestamp = int(time.time() * 1000)
        delta = (target_timestamp - now_timestamp) / 1000
        if delta > 0:
            time.sleep(delta)
        else:
            _LOGGER.warning(f"not sleeping ({delta * 1000} ms)")


if __name__ == "__main__":
    sensor_logger = SensorService()
    # while True:
    #     sensor_logger.log_sensor_data()
    sensor_logger.poll()
