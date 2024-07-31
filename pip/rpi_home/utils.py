import subprocess
import os
import json
import socket
from time import time
from typing import Any


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
    # try to get the name the quick way (on the local network)
    try:
        return socket.gethostbyname(socket.gethostname() + ".local")
    except socket.error:
        for line in get_lines_from_proc(["ip", "-o", "-4", "addr", "list"]):
            if "eth0" in line or "wlan0" in line:
                return line.split()[3].split("/")[0]

    # if we didn't get anything else... (but this probably return 127.0.1.1)
    return socket.gethostbyname(socket.gethostname())
