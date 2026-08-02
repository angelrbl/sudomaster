from pathlib import Path
from typing import Any
import json
import csv

from sudomaster.io import Exporter

class JSONExporter(Exporter):
    def export(self, data: dict[str, Any] | list[dict[str, Any]], filepath: str | Path) -> None:
        filepath = Path(filepath)

        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not data:
            filepath.touch()
            return

        with open(filepath, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

class CSVExporter(Exporter):
    def export(self, data: dict[str, Any] | list[dict[str, Any]], filepath: str | Path) -> None:
        filepath = Path(filepath)

        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not data:
            filepath.touch()
            return

        if type(data) != list:
            data = [data]

        fieldnames = list(data[0].keys())

        with open(filepath, mode="w", newline="", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)