import json
import logging
import time
import os

from .rpi_home_device import RpiHomeDevice
from .utils import timestamp
from .const import RPI_HOME_WWW_DIR

logger = logging.getLogger(__name__)


class RpiHomeSampler:
    def __init__(self):
        self.rpi_home_device = RpiHomeDevice()

        # set up the sampling parameters
        self.sampling_interval_ms = int(self.rpi_home_device.sampling_interval * 1000)
        self.start_timestamp = timestamp()
        self.counter = 0

        # clamp the starting time stamp to be an absolute multiple of the interval
        self.start_timestamp -= self.start_timestamp % self.sampling_interval_ms

    def sample(self):
        # print(json.dumps(self.rpi_home_device.report()))
        now_file = os.path.join(RPI_HOME_WWW_DIR, "now.json")
        with open(now_file, "w") as f:
            json.dump(self.rpi_home_device.report(), f)

        # compute the next sampling interval, and how long we need to sleep until then (if any)
        self.counter += 1
        target_timestamp = self.start_timestamp + (self.counter * self.sampling_interval_ms)
        now_timestamp = timestamp()
        delta = (target_timestamp - now_timestamp) / 1000
        if delta > 0:
            time.sleep(delta)
        else:
            logger.warning(f"not sleeping (behind target by {delta * 1000} ms)")

    def run(self):
        while True:
            self.sample()
