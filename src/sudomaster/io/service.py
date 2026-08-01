from typing import Any, TypeVar
from pathlib import Path
from datetime import datetime

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

def resolve_output_path(output_arg: str | None, ext: str, default_name: str, default_dir: str | Path = "./results/", seed: int | None = None) -> Path | None:
    if not output_arg:
        return 

    if seed:
        default_name = f"{default_name}_{seed}.{ext}"
    else:
        default_name = f"{default_name}_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.{ext}"
    
    if output_arg == "AUTO":
        return default_dir / default_name

    path = Path(output_arg)
    if path.is_dir():
        return path / default_name

    return path