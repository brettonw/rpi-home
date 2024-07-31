#!/usr/local/rpi_home/python3/bin/python3

import argparse
import logging
from time import sleep
from typing import cast

from const import RPI_HOME, _RPI_HOME_SERVICE, _ZEROCONF

from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf
)

_LOGGER = logging.getLogger(__name__)


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    print(f"service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        print(f"info from zeroconf.get_service_info: {info:r}")

        if info:
            addresses = [
                "%s:%d" % (addr, cast(int, info.port))
                for addr in info.parsed_scoped_addresses()
            ]
            print("  addresses: %s" % ", ".join(addresses))
            print("  weight: %d, priority: %d" % (info.weight, info.priority))
            print(f"  server: {info.server}")
            if info.properties:
                print("  properties are:")
                for key, value in info.properties.items():
                    print(f"    {key!r}: {value!r}")
            else:
                print("  no properties")
        else:
            print("  no info")
        print("\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)

    zeroconf = Zeroconf(ip_version=IPVersion.All)

    services = [_RPI_HOME_SERVICE]

    print(f"\nbrowsing for {RPI_HOME} service, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
