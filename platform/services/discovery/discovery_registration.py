#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket
import signal
import time
import sys

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import get_ip_address
from const import RPI_HOME, _SVC, _SVC_PROTOCOL_HTTP, _SVC_PROTOCOL_HTTP_PORT, _ZEROCONF

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    #logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

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
        logger.info("Unregistering ({message})...")
        zc.unregister_service(service_info)
        zc.close()
        sys.exit(0)

    def handle_sigint(signum, frame):
        cleanup("SIGINT")

    def handle_sigterm(signum, frame):
        cleanup("SIGTERM")

    # set up the prep to be able to stop the service
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    # start the actual discovery registration
    logger.info(f"Registering {RPI_HOME} service on {hostname} ({ip_address})")
    zc.register_service(service_info)
    while True:
        time.sleep(1)
