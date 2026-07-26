from abc import ABC, abstractmethod
from dataclasses import dataclass
from sudomaster.core import Board

@dataclass
class SolverResult:
    success: bool | None = None
    board: Board | None = None
    execution_time: float | None = None
    backtracks: int | None = None


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, board: Board) -> SolverResult:
        pass
