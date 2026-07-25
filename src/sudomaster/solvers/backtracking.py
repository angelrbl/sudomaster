from sudomaster.solvers import BaseSolver, SolverResult
from sudomaster.core import Board

class BacktrackingSolver(BaseSolver):
    def solve(self, board: Board) -> SolverResult:
        solver_result = SolverResult()
        return solver_result

    def _solve_backtracking(board: Board):
        ...    