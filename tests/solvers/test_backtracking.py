import pytest
from sudomaster.core import Board, parse_board_string
from sudomaster.solvers import BacktrackingSolver

@pytest.fixture
def solver():
    return BacktrackingSolver()

def test_solve_easy_sudoku(solver):
    board_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    board = parse_board_string(board_string=board_string)

    result = solver.solve(board=board)
    assert result.success is True
    assert result.board is not None
    assert result.board.is_solved() is True
    assert result.execution_time > 0


def test_solve_already_solved_sudoku(solver):
    board_string = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
    board = parse_board_string(board_string=board_string)

    result = solver.solve(board=board)
    assert result.success is True
    assert result.backtracks == 0

def test_solve_unsolvable_sudoku(solver):
    board_string = "550070000600195000098000060800060003400803001700020006060000280000419005000080079"
    board = parse_board_string(board_string=board_string)

    result = solver.solve(board=board)
    assert result.success is False
    assert result.board is None

def test_solve_does_not_mutate_original_board(solver):
    board_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    board = parse_board_string(board_string=board_string)

    board_clone = board.clone()
    
    solver.solve(board=board)

    assert board.grid == board_clone.grid

def test_backtrack_counter_increments(solver):
    board_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    board = parse_board_string(board_string=board_string)
    
    result = solver.solve(board=board)
    assert result.backtracks > 0