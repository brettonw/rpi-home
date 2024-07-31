#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import get_ip_address
from const import RPI_HOME, _RPI_HOME_SERVICE, _PATH, _RPI_HOME_SERVICE_PORT, _SVC_PROTOCOL_HTTP, _ZEROCONF

_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

    info = ServiceInfo(
        type_=_SVC_PROTOCOL_HTTP,
        name=_RPI_HOME_SERVICE,
        addresses=[socket.inet_aton(get_ip_address())],
        port=_RPI_HOME_SERVICE_PORT,
        properties={_PATH: RPI_HOME},
        server=socket.gethostname()
    )

    zc = Zeroconf(ip_version=IPVersion.V4Only)
    print(f"Registering {RPI_HOME} service, press Ctrl-C to exit...")
    zc.register_service(info)
    try:
        input("Press enter to exit...\n\n")
    finally:
        print("Unregistering...")
        zc.unregister_service(info)
        zc.close()
