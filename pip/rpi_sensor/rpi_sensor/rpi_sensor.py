from abc import ABC, abstractmethod


class RpiSensor(ABC):
    @classmethod
    @abstractmethod
    def report(cls) -> list[dict]:
        pass
