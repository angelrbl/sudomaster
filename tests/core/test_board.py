import pytest
from sudomaster import Board, parse_board_string

def test_board_initialization():
    target_board = Board(rows=9, cols=9, grid=[[0]*9 for _ in range(9)])
    default_board = Board()
    assert target_board == default_board

def test_get_and_set():
    board = Board()

    board.set(row=0, col=0, num=1)

    assert board.get(row=0, col=0) == 1

def test_parse_board_string_valid():
    board_string = "5.............................................................................001"

    target_board = Board()
    target_board.set(row=0, col=0, num=5)
    target_board.set(row=8, col=8, num=1)

    assert parse_board_string(board_string=board_string) == target_board

def test_parse_board_string_invalid_length():
    board_string = "5.................676767............................................................001"

    with pytest.raises(ValueError):
        parse_board_string(board_string=board_string) is not None

def test_parse_board_string_invalid_value():
    board_string = "5.................vivaespaña..................................................001"
    
    with pytest.raises(ValueError):
        parse_board_string(board_string=board_string) is not None
    

def test_is_valid_move_success():
    board = Board()
    
    assert board.is_valid_move(row=0, col=0, num=1) == True

def test_is_valid_move_fails_row():
    board = Board()
    board.set(row=0, col=0, num=1)

    assert board.is_valid_move(row=0, col=2, num=1) == False

def test_is_valid_move_fails_col():
    board = Board()
    board.set(row=0, col=0, num=1)
    
    assert board.is_valid_move(row=2, col=0, num=1) == False

def test_is_valid_move_fails_box():
    board = Board()
    board.set(row=0, col=0, num=1)
    
    assert board.is_valid_move(row=2, col=2, num=1) == False

def test_get_candidates_empty_cell():
    board = Board()

    assert board.get_candidates(row=0, col=0) == {1, 2, 3, 4, 5, 6, 7, 8, 9}

def test_get_candidates_occupied_cell():
    board = Board()
    board.set(row=0, col=0, num=1)

    assert board.get_candidates(row=0, col=0) == set()

def test_find_empty_cell_true():
    board_string = ".87654321246173985351928746128537694634892157795461832519286473472319568863745219"
    board = parse_board_string(board_string=board_string)

    assert board.find_empty_cell() == (0, 0)

def test_find_empty_cell_false():
    board_string = "187654321246173985351928746128537694634892157795461832519286473472319568863745219"
    board = parse_board_string(board_string=board_string)
    
    assert board.find_empty_cell() == None

def test_is_solved_true():
    board_string = "987654321246173985351928746128537694634892157795461832519286473472319568863745219"
    board = parse_board_string(board_string=board_string)

    assert board.is_solved() == True

def test_is_solved_false():
    board_string = "987654321246773985351928746128537694634892157795461832519286473472319568863745219"
    board = parse_board_string(board_string=board_string)
    
    assert board.is_solved() == False

def test_is_solved_false_when_incomplete():
    board = Board()

    assert board.is_solved() == False

def test_clone_independence():
    original_board = Board()
    cloned_board = original_board.clone()

    cloned_board.set(row=0, col=0, num=1)

    assert (cloned_board != original_board) == True