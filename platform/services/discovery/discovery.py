#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket
import signal
import time
import sys

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import RPI_HOME, RpiHomeDevice, DISPLAY_NAME, SERIAL_NUMBER, RPI_HOME_VERSION
from const import _SVC_PROTOCOL_HTTP, _SVC_PROTOCOL_HTTP_PORT, ZEROCONF

# Configure logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a custom logger
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logging.getLogger(RPI_HOME).setLevel(logging.DEBUG)
# logging.getLogger(ZEROCONF).setLevel(logging.DEBUG)

# load a rpi_home device
device = RpiHomeDevice()

# set up the zeroconf
zc = Zeroconf(ip_version=IPVersion.V4Only)

# set up the service
service_info = ServiceInfo(
    type_=_SVC_PROTOCOL_HTTP,
    name=f"{device.display_name}.{_SVC_PROTOCOL_HTTP}",
    addresses=[socket.inet_aton(device.ip_address)],
    port=_SVC_PROTOCOL_HTTP_PORT,
    properties={RPI_HOME: RPI_HOME_VERSION, SERIAL_NUMBER: device.serial_number},
    server=device.hostname
)


def cleanup(message: str):
    logger.info(f"Unregistering ({message})...")
    zc.unregister_service(service_info)
    zc.close()
    sys.exit(0)


def handle_sigint(signum, frame):
    cleanup(f"SIGINT - {signum}")


def handle_sigterm(signum, frame):
    cleanup(f"SIGTERM - {signum}")


# set up to stop the service when interrupted
signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigterm)

# start the actual discovery registration
logger.info(f"Registering {RPI_HOME} service on {device.hostname} ({device.ip_address})")
zc.register_service(service_info)
while True:
    time.sleep(1)
