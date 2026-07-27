from sudomaster.solvers import SudokuSolver, SolverResult
from sudomaster.core import Board
import time

class BacktrackingSolver(SudokuSolver):
    def __init__(self):
        self.backtracks = 0

    def solve(self, board: Board) -> SolverResult:
        self.backtracks = 0
        start_time = time.perf_counter()

        work_board = board.clone()
        success = self._solve_backtracking(board=work_board)

        execution_time = time.perf_counter() - start_time

        return SolverResult(
            success=success,
            board=work_board if success else None,
            execution_time=execution_time,
            backtracks=self.backtracks
        )

    def _solve_backtracking(self, board: Board) -> bool:
        empty_cell = board.find_empty_cell()
        if empty_cell is None:
            return True

        row, col = empty_cell
        for candidate in board.get_candidates(row=row, col=col):
            if board.is_valid_move(row=row, col=col, num=candidate):
                board.set(row=row, col=col, num=candidate)
                if self._solve_backtracking(board=board):
                    return True
                board.set(row=row, col=col, num=0)
                self.backtracks += 1

        return False

    def count_solutions(self, board: Board, limit: int = 2) -> int:
        empty_cell = board.find_empty_cell()
        
        if empty_cell is None:
            return 1

        row, col = empty_cell
        solutions = 0

        candidates = board.get_candidates(row=row, col=col)
        for candidate in candidates:
            if board.is_valid_move(row=row, col=col, num=candidate):
                board.set(row=row, col=col, num=candidate)
                solutions += self.count_solutions(board=board, limit=limit)
                board.set(row=row, col=col, num=0)
                if solutions >= limit:
                    break

        return solutions