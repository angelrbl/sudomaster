from typing import Any, TypeVar
from pathlib import Path
import time

from sudomaster.io import get_exporter, get_loader, get_serializer

T = TypeVar("T")

def save_data(obj: Any, filepath: str | Path) -> None:
    serializer = get_serializer(target=obj)
    data = serializer.serialize(obj=obj)

    exporter = get_exporter(filepath=filepath)
    exporter.export(data=data, filepath=filepath)

def load_data(filepath: str | Path, target_class: type[T]) -> T:
    loader = get_loader(filepath=filepath)
    data = loader.load(filepath=filepath)

    serializer = get_serializer(target=target_class)
    return serializer.deserialize(data=data)

def resolve_output_path(output_arg: str | None, difficulty: str, ext: str, seed: int | None = None) -> Path | None:
    if not output_arg:
        return 

    identifier = f"seed_{seed}" if seed is not None else f"time_{int(time.time())}"
    
    auto_filename = f"sudoku_{difficulty}_{identifier}.{ext}"
    default_dir = Path("./results")

    if output_arg == "AUTO":
        return default_dir / auto_filename

    path = Path(output_arg)
    if not path.suffix:
        return path / auto_filename

    return path