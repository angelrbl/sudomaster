import pytest

from sudomaster import Board, board_to_string
from sudomaster.io.serializers import BoardSerializer

def test_board_serializer_serialize():
    board = Board()

    serializer = BoardSerializer()
    serialized_board = serializer.serialize(obj=board)

    assert isinstance(serialized_board, dict)
    assert serialized_board["grid"] == board_to_string(board=board)

def test_board_serializer_deserialize():
    serialized_board = {"grid": "000000000000000000000000000000000000000000000000000000000000000000000000000000000"}

    serializer = BoardSerializer()
    deserialized_board = serializer.deserialize(data=serialized_board)

    assert isinstance(deserialized_board, Board)
    assert deserialized_board == Board()
