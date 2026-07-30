from pathlib import Path

from sudomaster import Board, resolve_output_path, save_data, load_data

def test_save_and_load_roundtrip(tmp_path):
    test_file = tmp_path / "sudoku_test.json"

    board = Board()

    save_data(obj=board, filepath=test_file)
    retrieved_board = load_data(filepath=test_file, target_class=Board)

    assert retrieved_board.grid == board.grid

def test_resolve_output_path_returns_none_if_no_output():
    file_path = resolve_output_path(output_arg=None, difficulty="easy", seed=67, ext="json")

    assert file_path is None

def test_resolve_output_path_auto_flag():
    file_path = resolve_output_path(output_arg="AUTO", difficulty="easy", seed=67, ext="json")

    assert file_path == Path("./results/sudoku_easy_67.json")

def test_resolve_output_path_directory_only():
    file_path = resolve_output_path(output_arg="./my_sudokus/", difficulty="easy", seed=67, ext="json")
    
    assert file_path == Path("./my_sudokus/sudoku_easy_67.json")

def test_resolve_output_path_explicit_file():
    file_path = resolve_output_path(output_arg="./my_sudokus/sudoku_easy_67.json", difficulty="easy", seed=67, ext="json")
    
    assert file_path == Path("./my_sudokus/sudoku_easy_67.json")