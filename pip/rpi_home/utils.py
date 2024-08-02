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
    return get_lines_from_proc(proc)[line].split(delimiter)


def get_float_field_from_proc(proc: str | list[str], line: int, field: int, delimiter: str | None = None) -> float:
    return float(get_fields_from_proc(proc, line, delimiter)[field])


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

    # if we didn't get anything else... (but this probably returns 127.0.1.1)
    try:
        logger.debug(f"trying to get IP address from `socket` using unqualified name")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        logger.debug(f"got IP address ({ip_address}) from `socket` using just '{hostname}'")
        return ip_address
    except socket.error as exc:
        logger.warning(f"failed to get IP address from `socket`: {exc}")

    # the absolute last fallback
    logger.debug(f"returning final fallback IP address ({ip_address})")
    return ip_address


def get_mac_address() -> str:
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 12, 2)])
