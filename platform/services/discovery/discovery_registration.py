#!/usr/local/rpi_home/python3/bin/python3

import argparse
import logging
import socket
from time import sleep

from zeroconf import IPVersion, ServiceInfo, Zeroconf
from const import RPI_HOME, _RPI_HOME_SERVICE, _PATH, _RPI_HOME_SERVICE_PORT, _SVC_PROTOCOL_HTTP, _ZEROCONF

_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

    info = ServiceInfo(
        _SVC_PROTOCOL_HTTP,
        _RPI_HOME_SERVICE,
        addresses=[socket.inet_aton(socket.gethostbyname(socket.gethostname()))],
        port=_RPI_HOME_SERVICE_PORT,
        properties={_PATH: f"/{RPI_HOME}/"},
        server=socket.gethostname()
    )

    zeroconf = Zeroconf(ip_version=IPVersion.All)
    print(f"Registering {RPI_HOME} service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()
