from typing import Any
from pathlib import Path
import time

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

def resolve_output_path(output_arg: str | None, difficulty_or_solved: str, ext: str, seed: int | None = None) -> Path | None:
    if not output_arg:
        return 

    identifier = f"seed_{seed}" if seed is not None else f"time_{int(time.time())}"

    auto_filename = f"sudoku_{difficulty_or_solved}_{identifier}.{ext}"
    default_dir = Path("./results")

    if output_arg == "AUTO":
        return default_dir / auto_filename

    path = Path(output_arg)
    if not path.suffix:
        return path / auto_filename

    return path