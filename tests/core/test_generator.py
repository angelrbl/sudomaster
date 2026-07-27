import pytest
from sudomaster import SudokuGenerator, BacktrackingSolver, Difficulty, GeneratedSudoku, Board

@pytest.fixture
def solver():
    return BacktrackingSolver()

def test_generator_returns_valid_dataclass_structure():
    generator = SudokuGenerator(seed=67)
    result = generator.generate()

    assert isinstance(result, GeneratedSudoku)
    assert isinstance(result.sudoku, Board)
    assert isinstance(result.solution, Board)
    assert result.difficulty == Difficulty.EASY

def test_generator_reproducibility_with_seed():
    generator1 = SudokuGenerator(seed=67)
    generator2 = SudokuGenerator(seed=67)

    sudoku1 = generator1.generate()
    sudoku2 = generator2.generate()

    assert sudoku1 == sudoku2

def test_generator_uniqueness_without_seed():
    generator1 = SudokuGenerator()
    generator2 = SudokuGenerator()

    sudoku1 = generator1.generate()
    sudoku2 = generator2.generate()

    assert sudoku1.sudoku != sudoku2.sudoku

def test_generated_solution_is_complete_and_valid():
    generator = SudokuGenerator(seed=5)
    result = generator.generate()

    assert result.solution.find_empty_cell() == None
    assert result.solution.is_solved() == True

def test_generated_sudoku_has_exactly_one_solution(solver):
    generator = SudokuGenerator(seed=6)
    result = generator.generate()

    solver_solution = solver.solve(board=result.sudoku)
    total_solutions = solver.count_solutions(board=result.sudoku) 

    assert result.solution == solver_solution.board
    assert total_solutions == 1

def test_generator_respects_difficulty_holes_easy():
    generator = SudokuGenerator(seed=7)
    difficulty = Difficulty.EASY

    result = generator.generate(difficulty=difficulty)

    empty_cells_count = sum(
        1
        for r in range(result.sudoku.rows)
        for c in range(result.sudoku.cols)
        if result.sudoku.get(r, c) == 0
    )

    assert empty_cells_count == difficulty.value

def test_generator_respects_difficulty_holes_medium():
    generator = SudokuGenerator(seed=7)
    difficulty = Difficulty.MEDIUM

    result = generator.generate(difficulty=difficulty)

    empty_cells_count = sum(
        1
        for r in range(result.sudoku.rows)
        for c in range(result.sudoku.cols)
        if result.sudoku.get(r, c) == 0
    )

    assert empty_cells_count == difficulty.value

def test_generator_respects_difficulty_holes_hard():
    generator = SudokuGenerator(seed=7)
    difficulty = Difficulty.HARD

    result = generator.generate(difficulty=difficulty)

    empty_cells_count = sum(
        1
        for r in range(result.sudoku.rows)
        for c in range(result.sudoku.cols)
        if result.sudoku.get(r, c) == 0
    )

    assert empty_cells_count == difficulty.value