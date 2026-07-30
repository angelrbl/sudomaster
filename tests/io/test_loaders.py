import json

from sudomaster.io.loaders import JSONDataLoader

def test_json_loader_reads_file(tmp_path):
    board_data = {"grid": "000000000000000000000000000000000000000000000000000000000000000000000000000000000"}
    test_file = tmp_path / "sudoku_test.json"

    with open(test_file, "w", encoding='utf-8') as f:
        json.dump(board_data, f)

    loader_data = JSONDataLoader().load(filepath=test_file)
    assert loader_data == board_data
