from pathlib import Path
from typing import Any
import json
import csv
import ast

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

class TXTDataLoader(DataLoader):
    def load(self, filepath: str | Path) -> dict[str, Any]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        data: dict[str, Any] = {}
        with open(filepath, mode="r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue

                key, value_str = line.split(":", 1)
                key = key.strip()
                value_str = value_str.strip()

                try:
                    data[key] = ast.literal_eval(value_str)
                except (ValueError, SyntaxError):
                    data[key] = value_str

        return data