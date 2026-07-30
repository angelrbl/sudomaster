import pytest

from sudomaster import get_exporter, get_loader, get_serializer, Board, UnsupportedObjectTypeError, UnsupportedFileFormatException
from sudomaster.io.exporters import JSONExporter
from sudomaster.io.loaders import JSONDataLoader
from sudomaster.io.serializers import BoardSerializer

def test_get_exporter_returns_correct_instance():
    exporter = get_exporter("test.json")
    assert isinstance(exporter, JSONExporter)

def test_get_exporter_raises_error_for_unknown_extension():
    with pytest.raises(UnsupportedFileFormatException):
        assert get_exporter("test.67")

def test_get_loader_returns_correct_instance():
    loader = get_loader(filepath="test.json")
    assert isinstance(loader, JSONDataLoader)

def test_get_loader_raises_error_for_unknown_extension():
    with pytest.raises(UnsupportedFileFormatException):
        get_loader("test.67")

def test_get_serializer_resolves_from_instance_and_class():
    board_instance = Board()
    serializer_from_class = get_serializer(target=Board)
    serializer_from_instance = get_serializer(target=board_instance)

    assert isinstance(serializer_from_class, BoardSerializer)
    assert isinstance(serializer_from_instance, BoardSerializer)

def test_get_serializer_raises_error_for_unregistered_type():
    with pytest.raises(UnsupportedObjectTypeError):
        get_serializer(target="a string")