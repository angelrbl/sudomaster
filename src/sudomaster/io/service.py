from typing import Any
from pathlib import Path
from datetime import datetime

from sudomaster.io import get_exporter, get_loader, get_serializer
from sudomaster.core import Board, GeneratedSudoku
from sudomaster.solvers import SolverResult

def save_data(obj: Any, filepath: str | Path) -> None:
    serializer = get_serializer(target=obj)
    data = serializer.serialize(obj=obj)

    exporter = get_exporter(filepath=filepath)
    exporter.export(data=data, filepath=filepath)

def load_data(filepath: str | Path, target_class: type | None = None) -> Any:
    loader = get_loader(filepath=filepath)
    data = loader.load(filepath=filepath)

    if target_class is None:
        if "sudoku" in data and "solution" in data:
            target_class = GeneratedSudoku
        elif "success" in data and "execution_time" in data:
            target_class = SolverResult
        else:
            target_class = Board

    serializer = get_serializer(target=target_class)
    return serializer.deserialize(data=data)

def resolve_output_path(output_arg: str | None, ext: str, default_name: str, default_dir: str | Path = Path("./results/"), seed: int | None = None) -> Path | None:
    if not output_arg:
        return 

    ext = ext.lstrip(".").lower()

    if seed:
        default_name = f"{default_name}_{seed}.{ext}"
    else:
        default_name = f"{default_name}_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.{ext}"
    
    if output_arg == "AUTO":
        return default_dir / default_name

    path = Path(output_arg)
    if not path.suffix:
        return path / default_name

    return path