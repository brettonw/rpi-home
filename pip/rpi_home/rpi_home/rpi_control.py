from abc import ABC, abstractmethod
from typing import Any


class RpiControl(ABC):
    @classmethod
    @abstractmethod
    def perform(cls, data: dict[str, Any]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def version(cls) -> str:
        pass
