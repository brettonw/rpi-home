from abc import ABC, abstractmethod
from typing import Any


class RpiSensor(ABC):
    @classmethod
    @abstractmethod
    def report(cls) -> list[dict[str, Any]] | None:
        pass
