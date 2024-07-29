#!/usr/local/rpi_home/python3/bin/python3

from rpi_home import RpiHomeSampler

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    RpiHomeSampler().run()
