from setuptools import setup, find_packages
import os


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "rpi_sensor", "version.py")
    with open(version_file) as f:
        exec(f.read())
    return locals()["RPI_HOME_VERSION"]


setup(
    name="rpi_sensor",
    version=get_version(),
    packages=find_packages(),
    install_requires=["homeassistant"]
)
