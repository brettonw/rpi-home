#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket
import signal
import time
import sys

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import get_ip_address
from const import RPI_HOME, _SVC, _SVC_PROTOCOL_HTTP, _SVC_PROTOCOL_HTTP_PORT, _ZEROCONF

_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

    # set up the zeroconf
    zc = Zeroconf(ip_version=IPVersion.V4Only)
    service_info = ServiceInfo(
        type_=_SVC_PROTOCOL_HTTP,
        name=f"{socket.gethostname()}.{_SVC_PROTOCOL_HTTP}",
        addresses=[socket.inet_aton(get_ip_address())],
        port=_SVC_PROTOCOL_HTTP_PORT,
        properties={_SVC: RPI_HOME},
        server=socket.gethostname()
    )

    def cleanup():
        _LOGGER.info("Unregistering...")
        zc.unregister_service(service_info)
        zc.close()

    def handle_sigint(signum, frame):
        _LOGGER.info("SIGINT received. Shutting down...")
        cleanup()
        sys.exit(0)

    def handle_sigterm(signum, frame):
        _LOGGER.info("SIGTERM received. Shutting down...")
        cleanup()
        sys.exit(0)

    # set up the prep to be able to stop the service
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    # start the actual discovery registration
    _LOGGER.info(f"Registering {RPI_HOME} service on {service_info.server}")
    zc.register_service(service_info)
    try:
        while True:
            time.sleep(1)
    finally:
        cleanup()
