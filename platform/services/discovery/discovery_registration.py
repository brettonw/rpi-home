#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket
import signal
import time
import sys

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import get_ip_address
from const import RPI_HOME, _SVC, _SVC_PROTOCOL_HTTP, _SVC_PROTOCOL_HTTP_PORT

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

# set up the zeroconf
zc = Zeroconf(ip_version=IPVersion.V4Only)
hostname = socket.gethostname()
ip_address = get_ip_address()

service_info = ServiceInfo(
    type_=_SVC_PROTOCOL_HTTP,
    name=f"{hostname}.{_SVC_PROTOCOL_HTTP}",
    addresses=[socket.inet_aton(ip_address)],
    port=_SVC_PROTOCOL_HTTP_PORT,
    properties={_SVC: RPI_HOME},
    server=hostname
)


def cleanup(message: str):
    logger.info(f"Unregistering ({message})...")
    zc.unregister_service(service_info)
    zc.close()
    sys.exit(0)


def handle_sigint(signum, frame):
    cleanup(f"SIGINT - {signum} {frame}")


def handle_sigterm(signum, frame):
    cleanup(f"SIGTERM - {signum} {frame}")


# set up the prep to be able to stop the service
signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigterm)

# start the actual discovery registration
logger.info(f"Registering {RPI_HOME} service on {hostname} ({ip_address})")
zc.register_service(service_info)
while True:
    time.sleep(1)
