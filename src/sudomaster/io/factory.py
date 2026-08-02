from pathlib import Path
from typing import Any
import pandas as pd

from sudomaster.core import Board, GeneratedSudoku
from sudomaster.solvers import SolverResult

from sudomaster.io import Exporter, DataLoader, Serializer
from sudomaster.io.exporters import JSONExporter, CSVExporter
from sudomaster.io.loaders import JSONDataLoader
from sudomaster.io.serializers import (
    BoardSerializer,
    GeneratedSudokuSerializer,
    SolverResultSerializer,
    DataFrameSerializer
)

class UnsupportedFileFormatException(Exception):
    """"Raised when trying to read/write an unsupported extension."""
    pass

class UnsupportedObjectTypeError(Exception):
    """Raised when trying to serialized an  object without an existing serializer."""
    pass

_EXPORTERS: dict[str, type[Exporter]] = {
    ".json": JSONExporter,
    ".csv": CSVExporter
}

_LOADERS: dict[str, type[DataLoader]] = {
    ".json": JSONDataLoader
}

_SERIALIZERS: dict[type, type[Serializer]] = {
    Board: BoardSerializer,
    GeneratedSudoku: GeneratedSudokuSerializer,
    SolverResult: SolverResultSerializer,
    pd.DataFrame: DataFrameSerializer
}

def get_exporter(filepath: str | Path) -> Exporter:
    ext = Path(filepath).suffix.lower()

    exporter_class = _EXPORTERS.get(ext)
    if not exporter_class:
        raise UnsupportedFileFormatException(f"Unsupported exporting format: {ext}")

    return exporter_class()

def get_loader(filepath: str | Path) -> DataLoader:
    ext = Path(filepath).suffix.lower()
    
    loader_class = _LOADERS.get(ext)
    if not loader_class:
        raise UnsupportedFileFormatException(f"Unsupported loading format: {ext}")

    return loader_class()

def get_serializer(target: Any) -> Serializer:
    if isinstance(target, type):
        target_type = target
    else:
        target_type = type(target)

    serializer_class = _SERIALIZERS.get(target_type)
    if not serializer_class:
        raise UnsupportedObjectTypeError(f"There is not a serializer for: {target_type.__name__}")

    return serializer_class()