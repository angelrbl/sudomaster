from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Board:
    rows: int = 9
    cols: int = 9
    grid: list[list[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.grid:
            self.grid = [[0] * self.cols for _ in range(self.rows)]

    def set(self, row: int, col:int, num:int) -> None:
        self.grid[row][col] = num

    def get(self, row: int, col:int) -> int:
        return self.grid[row][col]

    def is_valid_move(self, row: int, col:int, num: int) -> bool:
        if num in self.grid[row]:
            return False

        col_list = [self.grid[r][col] for r in range(self.rows)]
        if num in col_list:
            return False


        box_row_index = (row // 3) * 3
        box_col_index = (col // 3) * 3

        for r in range(box_row_index, box_row_index + 3):
            if num in self.grid[r][box_col_index:box_col_index + 3]:
                return False

        return True

    def get_candidates(self, row: int, col:int) -> set[int]:
        candidates = set()

        if self.grid[row][col] != 0:
            return candidates
        
        for num in range(1, 10):
            if self.is_valid_move(row=row, col=col, num=num):
                candidates.add(num)
        return candidates

    def find_empty_cell(self) -> tuple[int, int] | None:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.get(row=row, col=col) == 0:
                    return row, col
        return None

    def is_solved(self) -> bool:
        #Check 0's:
        if self.find_empty_cell() is not None:
            return False
        
        # Check rows
        for row in self.grid:
            nums = [num for num in row if num != 0]
            if len(set(nums)) != len(nums):
                return False

        # Check cols
        for col_index in range(self.cols):
            col = [r[col_index] for r in self.grid]
            nums = [num for num in col if num != 0]
            if len(set(nums)) != len(nums):
                return False

        # Check boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [
                    self.grid[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                nums = [num for num in box if num != 0]
                if len(set(nums)) != len(nums):
                    return False 
        
        return True

    def clone(self) -> Board:
        new_grid = [row[:] for row in self.grid]
        return Board(rows=self.rows, cols=self.cols, grid=new_grid)

def parse_board_string(board_string: str) -> Board:
    formatted_board_string = board_string.replace(".", "0")
    
    if len(board_string) != 81:
        raise ValueError("The length of the string must be 81 characters long.")
    if not formatted_board_string.isdigit():
        raise ValueError("The string must contain only the character '.' and numbers.")
    
    grid = []
    for board_slice in range(0, 81, 9):
        grid.append([int(value) for value in formatted_board_string[board_slice:board_slice+9]])

    board = Board(grid=grid)
    return board