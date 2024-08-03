import logging
import subprocess
import os
import json
import socket
import uuid
from time import time
from typing import Any

logger = logging.getLogger(__name__)


def get_lines_from_proc(proc: str | list[str]) -> list[str]:
    source = subprocess.run([proc] if isinstance(proc, str) else proc, capture_output=True, text=True)
    return [line for line in source.stdout.split("\n") if line]


def get_fields_from_proc(proc: str | list[str], line: int, delimiter: str | None = None) -> list[str]:
    lines = get_lines_from_proc(proc)
    return lines[line].split(delimiter) if len(lines) > line else []


def get_float_field_from_proc(proc: str | list[str], line: int, field: int, delimiter: str | None = None) -> float:
    fields = get_fields_from_proc(proc, line, delimiter)
    # XXX what should the fallback be?
    return float(fields[field]) if len(fields) > field else 0.0


def load_json_file(path: str) -> dict[str, Any] | None:
    if os.path.isfile(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def put_if_not_none(record: dict[str, Any], name: str, value: Any | None) -> Any:
    if value is not None:
        record[name] = value
    return value


def timestamp() -> int:
    return int(time() * 1000)


def get_ip_address() -> str:
    # start with the worst possible answer we can get
    ip_address = "127.0.0.1"

    # try to get the name the quick way (on the .local network)
    try:
        logger.debug(f"trying to get IP address from `socket` in '.local' network")
        qualified_hostname = socket.gethostname() + ".local"
        logger.debug(f"trying to get IP address from `socket` as '{qualified_hostname}'")
        ip_address = socket.gethostbyname(qualified_hostname)
        if ip_address != "127.0.0.1":
            logger.debug(f"got IP address ({ip_address}) from `socket` as '{qualified_hostname}'")
            return ip_address
        else:
            logger.debug(f"got useless IP address ({ip_address}) from `socket` as '{qualified_hostname}'")
    except socket.error as exc:
        logger.warning(f"failed to get IP address from `socket`: {exc}")

    # try the long way
    logger.debug(f"trying to get IP address from `ip -o -4 addr list`")
    for line in get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
        if "eth0" in line or "wlan0" in line:
            ip_address = line.split()[3].split("/")[0]
            logger.debug(f"got IP address ({ip_address}) from {line[:40]}...")
            return ip_address
    logger.debug(f"no functional interfaces found from `ip -o -4 addr list`")

    # if we didn't get anything else... (but this probably returns 127.0.1.1)
    try:
        logger.debug(f"trying to get IP address from `socket` using unqualified name")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        logger.debug(f"got IP address ({ip_address}) from `socket` using just '{hostname}'")
        return ip_address
    except socket.error as exc:
        logger.warning(f"failed to get IP address from `socket`: {exc}")

    # the absolute last fallback, if there was a socket exception for some reason
    logger.debug(f"returning final fallback IP address ({ip_address})")
    return ip_address


def get_serial_number() -> str:
    return get_fields_from_proc(["cat", "/sys/firmware/devicetree/base/serial-number"], -1)[0]
    # also consider `grep Serial /proc/cpuinfo`
    # or using vcgencmd otp_dump, lines 28-35 (ish)
    # note that we *could* burn the OTP registers to create a unique serial number for ourselves...
    # https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#otp-registers

def get_mac_address() -> dict[str, str]:
    macs = {}
    for interface in ["eth*", "wlan*"]:
        lines = get_lines_from_proc(["cat", f"/sys/class/net/{interface}/address"])
        field = get_fields_from_proc(["cat", f"/sys/class/net/{interface}/address"], 0)[0]
        if "cat" not in field:
            macs[interface] = field
    return macs
    # also consider this approach for generating a unique id
    # mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    # return ":".join([mac[e:e+2] for e in range(0, 12, 2)])

def get_os_description() -> str:
    for line in get_lines_from_proc(["lsb_release", "-a"]):
        if "Description" in line:
            return line.split(':')[1].strip()
    # if we didn't get anything else
    return "unknown"
