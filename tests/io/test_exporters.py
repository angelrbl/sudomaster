import json
from sudomaster.io.exporters import JSONExporter

def test_json_exporter_creates_valid_file(tmp_path):
    board_data = {"grid": "000000000000000000000000000000000000000000000000000000000000000000000000000000000"}
    test_file = tmp_path / "sudoku_test.json"

    JSONExporter().export(data=board_data, filepath=test_file)

    assert test_file.exists()

    with open(test_file, "r", encoding='utf-8') as f:
        loaded_data = json.load(f)

    assert loaded_data == board_data