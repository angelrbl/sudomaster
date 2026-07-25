from abc import ABC, abstractmethod
from dataclasses import dataclass
from sudomaster.core import Board

@dataclass
class SolverResult:
    success: bool
    board: Board | None
    execution_time: float | None
    backtracks: int | None


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, board: Board) -> SolverResult:
        pass
