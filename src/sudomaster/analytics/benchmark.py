from sudomaster.analytics import BenchmarkResult
from sudomaster.solvers import SudokuSolver
from sudomaster.core import Difficulty, SudokuGenerator

from dataclasses import asdict
import csv

def run_benchmark(
    solver_name: str,
    solver: SudokuSolver,
    difficulty: Difficulty,
    samples:int = 50 
) -> list[BenchmarkResult]:

    generator = SudokuGenerator()
    results = []

    for sample in range(samples):

        generated_sudoku = generator.generate(difficulty=difficulty)
        result = solver.solve(generated_sudoku.sudoku)

        results.append(
            BenchmarkResult(
                sample_id=sample,
                difficulty=generated_sudoku.difficulty,
                solver=solver_name,
                success=result.success,
                execution_time=result.execution_time,
                backtracks=result.backtracks
            )
        )

    return results