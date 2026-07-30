from pathlib import Path
from typing import Any
import json

from sudomaster.io import DataLoader

class JSONDataLoader(DataLoader):
    def load(self, filepath: str | Path) -> dict[str, Any] | list[dict[str, Any]]:
        filepath = Path(filepath)

        with open(filepath, "r", encoding='utf-8') as file:
            return json.load(file)