from enum import Enum
import random
from dataclasses import dataclass
from sudomaster.core import Board

class Difficulty(Enum):
    EASY = 26
    MEDIUM = 32
    HARD = 40

@dataclass(frozen=True)
class GeneratedSudoku:
    sudoku: Board
    solution: Board
    difficulty: Difficulty

class SudokuGenerator:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def generate(self, difficulty: Difficulty = Difficulty.EASY) -> GeneratedSudoku:
        #INITIALIZE EMPTY BOARD AND FILL IT RANDOMLY
        solved_board = Board()
        self._fill_board_randomly(board=solved_board)

        #CLONE THE SOLVED BOARD AND GENERATE A SUDOKU FROM IT
        unsolved_board = solved_board.clone()
        self._dig_holes(difficulty=difficulty, board=unsolved_board)

        #RETURN THE RESULT
        return GeneratedSudoku(
            sudoku=unsolved_board,
            solution=solved_board,
            difficulty=difficulty
        )


    def _fill_board_randomly(self, board: Board) -> bool:
        empty_cell = board.find_empty_cell()

        if empty_cell is None:
            return True

        row, col = empty_cell

        candidates = board.get_candidates(row=row, col=col)
        randomized_candidates = list(candidates)
        self.rng.shuffle(randomized_candidates)

        for candidate in randomized_candidates:
            if board.is_valid_move(row=row, col=col, num=candidate):
                board.set(row=row, col=col, num=candidate)
                if self._fill_board_randomly(board=board):
                    return True
                board.set(row=row, col=col, num=0)

        return False

    def _dig_holes(self, difficulty: Difficulty, board: Board) -> bool:
        holes = 0

        positions = [(r, c) for r in range(board.rows) for c in range(board.cols)]
        self.rng.shuffle(positions)

        for row, col in positions:
            if holes >= difficulty.value:
                break

            num = board.get(row=row, col=col)

            if num != 0:
                board.set(row=row, col=col, num=0)
                if self._count_solutions(board=board) != 1:
                    board.set(row=row, col=col, num=num)
                else:
                    holes += 1


    def _count_solutions(self, board: Board, limit: int = 2) -> int:
        empty_cell = board.find_empty_cell()
        
        if empty_cell is None:
            return 1

        row, col = empty_cell
        solutions = 0

        candidates = board.get_candidates(row=row, col=col)
        for candidate in candidates:
            if board.is_valid_move(row=row, col=col, num=candidate):
                board.set(row=row, col=col, num=candidate)
                solutions += self._count_solutions(board=board, limit=limit)
                board.set(row=row, col=col, num=0)
                if solutions >= limit:
                    break

        return solutions

if __name__ == "__main__":
    generator = SudokuGenerator()
    generated_sudoku = generator.generate()
    print(generated_sudoku)