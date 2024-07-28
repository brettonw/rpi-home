from setuptools import setup, find_packages
import os


module_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), module_name, "version.py")
    with open(version_file) as f:
        exec(f.read())
    return locals()["RPI_SENSOR_HOST_VERSION"]


setup(
    name=module_name,
    version=get_version(),
    packages=find_packages(),
    install_requires=["homeassistant", "rpi_sensor"]
)
