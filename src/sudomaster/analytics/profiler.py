from dataclasses import dataclass

from sudomaster.core import Difficulty

@dataclass(frozen=True)
class BenchmarkResult:
    sample_id: int
    difficulty: Difficulty
    solver: str
    success: bool
    execution_time: float
    backtracks: int