import toml
import os

from rpi_home import VERSION


def _get_version():
    pyproject_path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    with open(pyproject_path, "r") as pyproject_file:
        pyproject_data = toml.load(pyproject_file)
        return pyproject_data["project"][VERSION]

DRIVER_VERSION = _get_version()
