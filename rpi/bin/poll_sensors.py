#!/usr/local/rpi_home/python3/bin/python3

import json
import logging
import os
import time

from rpi_home import RpiHomeDevice, timestamp, RPI_HOME_WWW_DIR

_LOGGER = logging.getLogger(__name__)


class RpiHomeSamplingService:
    def __init__(self):
        self.rpi_home_device = RpiHomeDevice()
        self.sampling_interval_ms = int(self.rpi_home_device.sampling_interval * 1000)
        self.start_timestamp = timestamp()
        self.counter = 0

    def take_sample(self):
        print(json.dumps(self.rpi_home_device.report()))

        # now_file = os.path.join(RPI_HOME_WWW_DIR, "nowx.json")
        # with open(now_file, 'w') as f:
        #     json.dump(self.rpi_home_device.report(), f)

        self.counter += 1
        target_timestamp = self.start_timestamp + (self.counter * self.sampling_interval_ms)
        now_timestamp = timestamp()
        delta = (target_timestamp - now_timestamp) / 1000
        if delta > 0:
            time.sleep(delta)
        else:
            _LOGGER.warning(f"not sleeping ({delta * 1000} ms)")


if __name__ == "__main__":
    sampling_service = RpiHomeSamplingService()
    while True:
        sampling_service.take_sample()
