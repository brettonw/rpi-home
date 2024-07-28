from typing import Any

from rpi_home import RpiSensor, RpiSensorBuilder

class Driver(RpiSensor):
    @classmethod
    def report(cls) -> list[dict[str, Any]] | None:
        pass
