# sudomaster

**The ultimate Sudoku solver engine & performance analytics CLI.**

sudomaster is a Python engine and command-line tool built for solving, generating, and benchmarking Sudoku puzzles. It combines a constraint-based backtracking solver, a puzzle generator with five difficulty tiers, and a full analytics suite — with charts rendered directly in the terminal — all wrapped in a polished [Click](https://click.palletsprojects.com/) CLI.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Board string format](#board-string-format)
- [License](#license)

---

## Overview

sudomaster is organized around four CLI commands, exposed via the `sudomaster` console script:

| Command | Purpose |
|---|---|
| **generate** | Generate a new, uniquely-solvable Sudoku at a chosen difficulty. |
| **solve** | Solve a given Sudoku with a selected solver (currently backtracking). |
| **benchmark** | Run a solver against many generated puzzles and collect performance stats. |
| **plot** | Visualize benchmark metrics (bar charts, scatter, histogram) from a saved file. |

Running `sudomaster` with no arguments shows an ASCII banner and a table of these commands.

## Features

- 🧠 **Backtracking solver** with backtrack counting, execution timing, and a `count_solutions()` check used to verify puzzle uniqueness.
- 🎲 **Puzzle generator** that fills a board at random and digs holes one at a time, only keeping a removal if the puzzle still has exactly one solution.
- 🎯 **Five difficulty tiers** — `easy`, `medium`, `hard`, `expert`, `master` — based on the number of empty cells.
- 📊 **Benchmarking suite** that runs a solver across N generated puzzles per difficulty and aggregates success rate, execution time, and backtracks with pandas.
- 📈 **Terminal-native charts** (via `plotext`) — execution time and backtracks by difficulty, backtracks-vs-time scatter, and time-distribution histograms.
- 💾 **Pluggable I/O layer** (factory + strategy pattern) — export/import puzzles and results as JSON, CSV, or TXT, auto-selected by file extension and object type.
- 💻 **Interactive CLI** built with Click and Rich — missing options are prompted for interactively, and results are rendered as formatted boards in the terminal.

> ℹ️ Some CLI options and output formats may expand as the project evolves. This README describes each command based on the current implementation of `ui/cli.py` and `ui/crud.py`.

## Tech stack

| Category | Technology |
|---|---|
| Language | Python |
| CLI framework | [Click](https://click.palletsprojects.com/) |
| Terminal UI | [Rich](https://github.com/Textualize/rich) |
| Data handling | [Pandas](https://pandas.pydata.org/) |
| Terminal charts | [Plotext](https://github.com/piccolomo/plotext) |
| Testing | [Pytest](https://docs.pytest.org/) |

## Project structure

```
sudomaster/
├── src/
│   └── sudomaster/
│       ├── core/              # Board model, puzzle generator, difficulty levels
│       │   ├── board.py
│       │   └── generator.py
│       ├── solvers/           # Solver interface + backtracking implementation
│       │   ├── base.py
│       │   └── backtracking.py
│       ├── analytics/         # Benchmarking engine + result dataclasses
│       │   ├── benchmark.py
│       │   └── profiler.py
│       ├── io/                # Export/import: factory + strategy pattern
│       │   ├── exporters.py
│       │   ├── loaders.py
│       │   ├── serializers.py
│       │   ├── protocols.py
│       │   ├── factory.py
│       │   └── service.py
│       ├── ui/                # CLI, terminal rendering, and charts
│       │   ├── cli.py
│       │   ├── crud.py
│       │   ├── welcome.py
│       │   ├── charts.py
│       │   └── renderer.py
│       └── main.py            # Entry point: from sudomaster.ui import cli
├── tests/                      # Unit tests (pytest)
├── pyproject.toml              # Package configuration and CLI entry point
├── requirements.txt            # Project dependencies
└── LICENSE
```

## Installation

### Prerequisites

- Python 3.10 or higher

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/angelrbl/sudomaster.git
   cd sudomaster
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the package (registers the `sudomaster` command):

   ```bash
   pip install -e .
   ```

## Usage

Once installed, run `sudomaster --help` to see the available commands, or invoke it with no arguments to see the welcome screen.

### Generate a puzzle

```bash
sudomaster generate --difficulty hard
sudomaster generate -d expert --seed 42 --raw
sudomaster generate -d medium -o ./results/ --solution
```

| Option | Alias | Description |
|---|---|---|
| `--difficulty` | `-d` | `easy` \| `medium` \| `hard` \| `expert` \| `master` |
| `--output` | `-o` | Output path, e.g. `./results/sudoku_easy_1.json` |
| `--raw` | `-r` | Print the puzzle as an 81-character string |
| `--seed` | — | Integer seed for reproducible generation |
| `--solution` | `-s` | Also print/export the puzzle's solution |

### Solve a puzzle

```bash
sudomaster solve --file ./results/sudoku_easy_1.json
sudomaster solve --raw   # then paste the puzzle string when prompted
```

| Option | Alias | Description |
|---|---|---|
| `--file` | `-f` | Input file with the puzzle to solve |
| `--output` | `-o` | Output path for the solved result |
| `--raw` | `-r` | Print the solution as an 81-character string |
| `--solver` | `-s` | Solver to use — currently `backtracking` |

### Run a benchmark

```bash
sudomaster benchmark -s backtracking -d hard -n 100 --chart
sudomaster benchmark -d all -n 200 -o ./results/benchmarks/
```

| Option | Alias | Description |
|---|---|---|
| `--solver` | `-s` | Solver to benchmark — currently `backtracking` |
| `--difficulty` | `-d` | `easy` \| `medium` \| `hard` \| `expert` \| `master` \| `all` |
| `--samples` | `-n` | Number of puzzles to generate and solve |
| `--output` | `-o` | Output path for the raw results (CSV by default) |
| `--chart` | `-c` | Render terminal charts after the benchmark completes |

### Plot saved benchmark results

```bash
sudomaster plot ./results/benchmarks/benchmark_backtracking_hard.csv --type summary
sudomaster plot ./results/benchmarks/benchmark_backtracking_hard.csv -t dist
```

| Argument / Option | Alias | Description |
|---|---|---|
| `FILEPATH` (positional) | — | Path to a saved benchmark CSV |
| `--type` | `-t` | `summary` (bar charts) \| `scatter` (backtracks vs. time) \| `dist` (time histogram) |

### As a Python library

```python
from sudomaster.core.board import parse_board_string, board_to_string
from sudomaster.core.generator import SudokuGenerator, Difficulty
from sudomaster.solvers.backtracking import BacktrackingSolver

board = parse_board_string(
    "530.7....6..195....98....6.8...6...3.4..8.3..1...2...6....6...28....419..5....8.."
)

solver = BacktrackingSolver()
result = solver.solve(board)

if result.success:
    print(board_to_string(result.board))
    print(f"Solved in {result.execution_time:.4f}s with {result.backtracks} backtracks")

generator = SudokuGenerator(seed=42)
generated = generator.generate(difficulty=Difficulty.HARD)
print(board_to_string(generated.sudoku))
print(board_to_string(generated.solution))
```

## Board string format

Puzzles are represented as an **81-character string**, read row by row (9 rows × 9 columns):

- Digits `1`–`9` represent filled cells.
- `0` **or** `.` represent empty cells (both are normalized internally).
- The string must be exactly 81 characters long, or `parse_board_string()` raises a `ValueError`.

```text
530.7....6..195....98....6.8...6...3.4..8.3..1...2...6....6...28....419..5....8..
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Built by <a href="https://github.com/angelrbl">@angelrbl</a>
</div>
