from sudomaster.analytics import BenchmarkResult
from sudomaster.solvers import SudokuSolver
from sudomaster.core import Difficulty, SudokuGenerator

from dataclasses import asdict
import pandas as pd
import random
from typing import Callable

def run_benchmark(
    solver_name: str,
    solver: SudokuSolver,
    difficulty: Difficulty | None,
    on_progress: Callable[[], None] | None = None,
    samples:int | None = None 
) -> list[BenchmarkResult]:

    if samples is None:
        samples = 50 

    generator = SudokuGenerator()
    results = []

    for sample in range(samples):

        if on_progress:
            on_progress()

        generated_sudoku = generator.generate(difficulty=(difficulty if difficulty else random.choice(list(Difficulty))))
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

def benchmark_to_dataframe(results: list[BenchmarkResult]) -> pd.DataFrame:
    data = []
    for r in results:
        row = asdict(r)
        row["difficulty"] = str(r.difficulty.name)
        data.append(row)

    return pd.DataFrame(data)

def get_summary_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    summary_df = df.groupby("difficulty").agg(
        samples=("sample_id", "count"),
        avg_time_s=("execution_time", "mean"),
        max_time_s=("execution_time", "max"),
        avg_backtracks=("backtracks", "mean"),
        success_pct=("success", lambda s: s.mean() * 100)
    ).round(4)

    return summary_df