from pathlib import Path
import json
from typing import Any

from sudomaster.io import Exporter

class JSONExporter(Exporter):
    def export(self, data: dict[str, Any] | list[dict[str, Any]], filepath: str | Path) -> None:
        filepath = Path(filepath)

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)