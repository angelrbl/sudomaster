from pathlib import Path
from typing import Any, Protocol

class DataLoader(Protocol):
    def load(self, filepath: str | Path) -> dict[str, Any] | list[dict[str, Any]]:
        ...

class Serializer(Protocol):
    def serialize(self, obj: Any) -> dict[str, Any]:
        ...

    def deserialize(self, data: dict[str, Any]) -> Any:
        ...

class Exporter(Protocol):
    def export(self, data: dict[str, Any] | list[dict[str, Any]], filepath: str | Path) -> None:
        ...