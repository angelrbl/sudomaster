from sudomaster.solvers import BaseSolver, SolverResult
from sudomaster.core import Board
import time

class BacktrackingSolver(BaseSolver):
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

    def _solve_backtracking(self, board: Board):
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