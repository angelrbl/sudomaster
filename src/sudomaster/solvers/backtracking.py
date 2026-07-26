from sudomaster.solvers import BaseSolver, SolverResult
from sudomaster.core import Board, parse_board_string

class BacktrackingSolver(BaseSolver):
    def __init__(self):
        self.backtracks = 0

    def solve(self, board: Board) -> SolverResult:
        solver_result = SolverResult()
        solved = self._solve_backtracking(board=board)
        solver_result.success = solved
        return solver_result

    def _solve_backtracking(self, board: Board):
        is_full = True
        for row in board.grid:
            if 0 in row:
                is_full = False

        if is_full:
            return board.is_solved()

        for row in range(board.rows):
            for col in range(board.cols):
                if board.grid[row][col] == 0:
                    for candidate in board.get_candidates(row=row, col=col):
                        if board.is_valid_move(row=row, col=col, num=candidate):
                            board.set(row=row, col=col, num=candidate)
                            if self._solve_backtracking(board=board):
                                return True
                            board.set(row=row, col=col, num=0)
        
                            return False

if __name__ == "__main__":
    board = parse_board_string(board_string="52...6.........7.13...........4..8..6......5...........418.........3..2...87.....")
    solver = BacktrackingSolver()
    print(solver.solve(board=board))