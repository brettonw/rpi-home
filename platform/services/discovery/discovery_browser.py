#!/usr/local/rpi_home/python3/bin/python3

# this is really just a test program to debug zeroconf

import logging

from zeroconf import (Zeroconf, IPVersion, ServiceBrowser, ServiceListener)
from const import RPI_HOME, _PATH_UTF8, _SVC_PROTOCOL_HTTP, _RPI_HOME_SERVICE, _ZEROCONF

class DiscoveryHandler(ServiceListener):
    def _report(self, zc: Zeroconf, service_type: str, service_name: str):
        info = zc.get_service_info(service_type, service_name)
        if info is not None:
            path = info.properties[_PATH_UTF8]
            for key, value in info.properties.items():
                #if key == info.properties.:
                #    path = value.decode("utf-8")
                print(f"    {str(key)}: {str(value)}")
            print("  addresses: %s" % ", ".join([f"{addr}:{info.port}/{path}/" for addr in info.parsed_scoped_addresses()]))
            print(f"  server: {info.server}")
        else:
            print("  no info")
        print("\n")

    def add_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        print(f"add_service ({service_type}, {service_name})")
        if service_name == _RPI_HOME_SERVICE:
            self._report(zc, service_type, service_name)

    def update_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        print(f"update_service ({service_type}, {service_name})")
        if service_name == _RPI_HOME_SERVICE:
            self._report(zc, service_type, service_name)

    def remove_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        print(f"remove_service ({service_type}, {service_name})")
        if service_name == _RPI_HOME_SERVICE:
            self._report(zc, service_type, service_name)

    def browse(self):
        print(f"\nbrowsing for {RPI_HOME} service, press Ctrl-C to exit...\n")
        zc = Zeroconf(ip_version=IPVersion.V4Only)
        logging.getLogger(_ZEROCONF).setLevel(logging.DEBUG)
        ServiceBrowser(zc, _SVC_PROTOCOL_HTTP, DiscoveryHandler())
        try:
            input("Press enter to exit...\n\n")
        finally:
            zc.close()


if __name__ == "__main__":
    DiscoveryHandler().browse()
