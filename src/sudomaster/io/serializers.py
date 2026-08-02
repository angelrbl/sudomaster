from typing import Any
import pandas as pd
import json
import ast
from sudomaster.core import Difficulty, GeneratedSudoku, Board, parse_board_string, board_to_string
from sudomaster.solvers import SolverResult
from sudomaster.io import Serializer

class BoardSerializer(Serializer):
    def serialize(self, obj: Board) -> dict[str, str]:
        board_string = board_to_string(board=obj)
        return {"grid": board_string}

    def deserialize(self, data: dict[str, str] | str) -> Board:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = ast.literal_eval(data)
        board_string = data.get("grid")
        return parse_board_string(board_string=board_string)

class GeneratedSudokuSerializer(Serializer):
    def __init__(self, board_serializer: BoardSerializer | None = None) -> None:
        self.board_serializer = board_serializer or BoardSerializer()
        
    def serialize(self, obj: GeneratedSudoku) -> dict[str, Any]:
        return {
            "sudoku": self.board_serializer.serialize(obj=obj.sudoku),
            "solution": self.board_serializer.serialize(obj=obj.solution),
            "difficulty": obj.difficulty.name.lower()
        }

    def deserialize(self, data: dict[str, Any]) -> GeneratedSudoku:
        raw_difficulty = data.get("difficulty", "easy").upper()

        return GeneratedSudoku(
            sudoku=self.board_serializer.deserialize(data=data["sudoku"]),
            solution=self.board_serializer.deserialize(data=data["solution"]),
            difficulty=Difficulty[raw_difficulty]
        )

class SolverResultSerializer(Serializer):
    def __init__(self, board_serializer: BoardSerializer | None = None) -> None:
        self.board_serializer = board_serializer or BoardSerializer()
          
    def serialize(self, obj: SolverResult) -> dict[str, Any]:
        board_data = None
        if obj.board:
            board_data = self.board_serializer.serialize(obj=obj.board)

        return {
            "success": obj.success,
            "board": board_data,
            "backtracks": obj.backtracks,
            "execution_time": obj.execution_time
        }

    def deserialize(self, data: dict[str, Any]) -> SolverResult:
        success = data.get("success")
        board_data = data.get("board", None)
        backtracks = data.get("backtracks", None)
        execution_time = data.get("execution_time", None)

        board = self.board_serializer.deserialize(data=board_data) if board_data else None

        return SolverResult(
            success=success,
            board=board,
            backtracks=backtracks,
            execution_time=execution_time
        )      

class DataFrameSerializer(Serializer):
    def __init__(self):
        self.DIFFICULTY_ORDER = ["easy", "medium", "hard", "expert", "master"]

    def serialize(self, obj: pd.DataFrame) -> list[dict[str, Any]]:
        return obj.to_dict(orient="records")

    def deserialize(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)

        if "difficulty" in df.columns:
            df["difficulty"] = pd.Categorical(
                df["difficulty"].astype(str).str.lower(),
                categories=self.DIFFICULTY_ORDER,
                ordered=True
            )

        for col in df.columns:
            if col != "difficulty":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df