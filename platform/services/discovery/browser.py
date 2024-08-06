#!/usr/local/rpi_home/python3/bin/python3

# this is really just a test program to debug zeroconf

import logging
import subprocess
import threading

from typing import NamedTuple
from time import sleep

from rpi_home import RPI_HOME_VERSION, RPI_HOME, VERSION
from zeroconf import (Zeroconf, IPVersion, ServiceBrowser, ServiceListener)
from const import _SVC_PROTOCOL_HTTP, ZEROCONF


class DiscoveryAction(NamedTuple):
    action: str
    service_name: str

    def report(self):
        print(f"{self.action} ({self.service_name[:-(len(_SVC_PROTOCOL_HTTP) + 1)]})")


class DiscoveryHandler(ServiceListener):
    @staticmethod
    def _report_and_update_rpi_home_device(zc: Zeroconf, discovery_action: DiscoveryAction):
        info = zc.get_service_info(_SVC_PROTOCOL_HTTP, discovery_action.service_name)
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

        # check to see if this is a rpi_home service and if it needs to be updated
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

    def __init__(self):
        # shared work queue and a synchronizing primitive for it
        self.work_queue: list[DiscoveryAction] = []
        self.work_queue_lock = threading.Lock()

    def enqueue(self, discovery_action: DiscoveryAction):
        with self.work_queue_lock:
            self.work_queue.append(discovery_action)

    def dequeue(self) -> DiscoveryAction | None:
        with self.work_queue_lock:
            return self.work_queue.pop() if len(self.work_queue) > 0 else None

    def perform(self, zc: Zeroconf):
        discovery_action = self.dequeue()
        while discovery_action is not None:
            discovery_action.report()
            if (discovery_action.action == "add") or (discovery_action.action == "update"):
                self._report_and_update_rpi_home_device(zc, discovery_action)
            discovery_action = self.dequeue()

    def add_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("add", service_name))

    def update_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("update", service_name))

    def remove_service(self, zc: Zeroconf, service_type: str, service_name: str) -> None:
        self.enqueue(DiscoveryAction("remove", service_name))

    def browse(self):
        zc = Zeroconf(ip_version=IPVersion.V4Only)
        logging.getLogger(ZEROCONF).setLevel(logging.DEBUG)
        ServiceBrowser(zc, _SVC_PROTOCOL_HTTP, self)
        print(f"\nbrowsing for {_SVC_PROTOCOL_HTTP} services (press [ctrl-c] to stop)...")
        try:
            while True:
                self.perform(zc)
                sleep(1)
        except KeyboardInterrupt:
            print("stopping...")
        finally:
            zc.close()


print(f"starting up with {RPI_HOME} {VERSION}: {RPI_HOME_VERSION}")
DiscoveryHandler().browse()
