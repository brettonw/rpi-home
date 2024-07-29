import logging
import subprocess
import sys
import os
import importlib

from .const import RPI_HOME_ROOT_DIR, DRIVER_PREFIX
from .rpi_sensor import RpiSensor

_LOGGER = logging.getLogger(__name__)


def import_class_from_driver(driver: str, class_name: str) -> RpiSensor | None:
    # condition the module name to start with "rpi_home_"
    if not driver.startswith(DRIVER_PREFIX):
        driver = DRIVER_PREFIX + driver

    # try to load the module
    try:
        imported_module = importlib.import_module(driver)
    except ModuleNotFoundError:
        _LOGGER.error(f"module ({driver}) not found.")
        return None

    # try to get the requested class
    try:
        imported_class = getattr(imported_module, class_name)
    except AttributeError:
        _LOGGER.error(f"class ({class_name}) not found in module '{driver}'.")
        return None

    # ensure that the found attribute is a subclass of RpiSensor
    if not issubclass(imported_class, RpiSensor):
        print(f"class ({class_name}) in module ({driver}) is not an RpiSensor subclass.")
        return None

    return imported_class


def install_driver(driver: str, class_name: str) -> RpiSensor | None:
    # use pip to install or upgrade the module
    try:
        module_path = os.path.join(RPI_HOME_ROOT_DIR, "rpi", "drivers", driver)
        _LOGGER.debug(f"installing driver ({driver})")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', module_path])
        _LOGGER.debug(f"  installed driver ({driver})")
    except subprocess.CalledProcessError as e:
        _LOGGER.error(f"failed to install or upgrade module for driver ({driver}): {e}")

    # fetch the installed module and return the driver class
    return import_class_from_driver(driver, class_name)
