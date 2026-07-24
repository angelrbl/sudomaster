from dataclasses import dataclass, field

@dataclass
class Board:
    rows: int = 9
    cols: int = 9
    grid: list[list[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.grid:
            self.grid = [[0] * self.cols for _ in range(self.rows)]

    def is_valid_move(self, row: int, col:int, num: int) -> bool:
        if num in self.grid[row]:
            return False

        col_list = [self.grid[r][col] for r in range(self.rows)]
        if num in col_list:
            return False


        cell_row = row // 3
        cell_col = col // 3

        for r in range(cell_row, cell_row + 3):
            if num in self.grid[r][cell_col:cell_col + 3]:
                return False

        return True

    def get_candidates(self, row: int, col:int) -> set[int]:
        candidates = set()
        for num in range(1, 9):
            if self.is_valid_move(row=row, col=col, num=num):
                candidates.add(num)
        return candidates

    def is_solved(self) -> bool:
        for row in self.rows:
            for col in self.cols:
                num = self.grid[row][col]
                if num == 0 or not self.is_valid_move(row=row, col=col, num=num):
                    return False
        return True

    def clone(self) -> Board:
        return Board(rows=self.rows, cols=self.cols, grid=self.grid)