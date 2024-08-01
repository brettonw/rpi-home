#!/usr/local/rpi_home/python3/bin/python3

import logging
import socket

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from rpi_home import get_ip_address
from const import RPI_HOME, _SVC, _SVC_PROTOCOL_HTTP, _SVC_PROTOCOL_HTTP_PORT, _ZEROCONF

_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

    service_info = ServiceInfo(
        type_=_SVC_PROTOCOL_HTTP,
        name=f"{socket.gethostname()}.{_SVC_PROTOCOL_HTTP}",
        addresses=[socket.inet_aton(get_ip_address())],
        port=_SVC_PROTOCOL_HTTP_PORT,
        properties={_SVC: RPI_HOME},
        server=socket.gethostname()
    )

    zc = Zeroconf(ip_version=IPVersion.V4Only)
    print(f"Registering {RPI_HOME} service on {service_info.server}")
    zc.register_service(service_info)
    try:
        input("Press [enter] to stop...\n\n")
    finally:
        print("Unregistering...")
        zc.unregister_service(service_info)
        zc.close()
