#!/usr/local/rpi_home/python3/bin/python3

# this is really just a test program to debug zeroconf

import logging
import subprocess

from rpi_home import RPI_HOME_VERSION, RPI_HOME, VERSION
from zeroconf import (Zeroconf, IPVersion, ServiceBrowser, ServiceListener, ServiceInfo)
from const import _SVC_PROTOCOL_HTTP, ZEROCONF


class DiscoveryHandler(ServiceListener):
    @staticmethod
    def _short_report(action: str, service_name: str):
        print(f"{action} ({service_name[:-(len(_SVC_PROTOCOL_HTTP) + 1)]})")

    @staticmethod
    def _report(zc: Zeroconf, action: str, service_name: str):
        DiscoveryHandler._short_report(action, service_name)
        info = zc.get_service_info(_SVC_PROTOCOL_HTTP, service_name)
        if info is not None:
            addresses = info.parsed_scoped_addresses()
            port = f":{info.port}" if int(info.port) != 80 else ""
            print("  address" + ("es" if len(addresses) > 1 else "") + ": " +
                  ", ".join([f"{address}{port}" for address in addresses]))
            host: str = info.server[:-1] if info.server.endswith(".") else info.server
            host = (host[:-6] if host.endswith(".local") else host).lower()
            print(f"  host: {host}")
            if (info.properties is not None) and (len(info.properties.keys()) > 0):
                preface = "  properties:\n    "
                for key, value in info.properties.items():
                    if value is not None:
                        print(f"{preface}{key.decode("utf-8")}: {value.decode("utf-8") if isinstance(value, bytes) else value}")
                        preface = "    "
        else:
            print("  no info")
        print()

    def add_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self._report(zc, "add", service_name)

        # check to see if a rpi_home service should be updated
        info = zc.get_service_info(_SVC_PROTOCOL_HTTP, service_name)
        if (info is not None) and (info.properties is not None) and (len(info.properties.keys()) > 0):
            for key, value in info.properties.items():
                if value is not None:
                    if (key.decode("utf-8") == RPI_HOME) and (value.decode("utf-8") != RPI_HOME_VERSION):
                        try:
                            host: str = info.server[:-1] if info.server.endswith(".") else info.server
                            print(f"UPDATE {host} at version {value.decode("utf-8")}")
                            ssh_command = ["ssh", host, "/usr/local/rpi_home/platform/bin/update_instance.bash"]
                            subprocess.run(ssh_command, capture_output=False, text=True, check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"failed to execute command: {e}")
                        print()

    def update_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self._short_report("update", service_name)

    def remove_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self._short_report("remove", service_name)

    def browse(self):
        zc = Zeroconf(ip_version=IPVersion.V4Only)
        logging.getLogger(ZEROCONF).setLevel(logging.DEBUG)
        ServiceBrowser(zc, _SVC_PROTOCOL_HTTP, self)
        print(f"\nbrowsing for {_SVC_PROTOCOL_HTTP} services")
        try:
            input("  press [enter] to stop...\n\n")
        finally:
            zc.close()


print(f"starting up with {RPI_HOME} {VERSION}: {RPI_HOME_VERSION}")
DiscoveryHandler().browse()
