import logging
import json
from typing import Any
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class RpiHomeApi:
    @staticmethod
    def now(self, host: str) -> dict[str, Any]:
        with urlopen(Request(f"http://{host}/now.json")) as response:
            return json.loads(response.read().decode())
