from pathlib import Path
from typing import Any
import json
import csv

from sudomaster.io import DataLoader

class JSONDataLoader(DataLoader):
    def load(self, filepath: str | Path) -> dict[str, Any] | list[dict[str, Any]]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding='utf-8') as file:
            return json.load(file)

class CSVDataLoader(DataLoader):
    def load(self, filepath: str | Path) -> dict[str, Any] | list[dict[str, Any]]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = [dict(row) for row in reader]
            if len(data) > 1:
                return data
            else:
                return data[0]