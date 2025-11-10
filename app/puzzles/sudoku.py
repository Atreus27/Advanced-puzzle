"""
Sudoku generator + solver (simple backtracking approach)
Generates a unique puzzle and solves it recursively.
"""
from copy import deepcopy
import random
from typing import List, Optional

Grid = List[List[int]]

class Sudoku:
    def __init__(self, size: int = 9):
        assert size == 9, "Only 9x9 Sudoku supported."
        self.size = size
        self.box = 3

    def _valid(self, grid: Grid, r: int, c: int, val: int) -> bool:
        if any(grid[r][j] == val for j in range(self.size)): return False
        if any(grid[i][c] == val for i in range(self.size)): return False
        br, bc = (r // self.box) * self.box, (c // self.box) * self.box
        for i in range(br, br + self.box):
            for j in range(bc, bc + self.box):
                if grid[i][j] == val:
                    return False
        return True

    def solve(self, grid: Grid) -> Optional[Grid]:
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    for v in range(1, 10):
                        if self._valid(grid, i, j, v):
                            grid[i][j] = v
                            sol = self.solve(grid)
                            if sol is not None:
                                return sol
                            grid[i][j] = 0
                    return None
        return deepcopy(grid)

    def _fill_grid(self, grid: Grid) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self._valid(grid, i, j, n):
                            grid[i][j] = n
                            if self._fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def _has_unique_solution(self, grid: Grid, max_count: int = 2) -> bool:
        count = 0
        def backtrack(g):
            nonlocal count
            if count >= max_count: return
            for i in range(self.size):
                for j in range(self.size):
                    if g[i][j] == 0:
                        for v in range(1, 10):
                            if self._valid(g, i, j, v):
                                g[i][j] = v
                                backtrack(g)
                                g[i][j] = 0
                        return
            count += 1
        backtrack(grid)
        return count == 1

    def generate(self, difficulty: str = "medium") -> Grid:
        grid: Grid = [[0] * self.size for _ in range(self.size)]
        self._fill_grid(grid)
        levels = {"easy": 36, "medium": 30, "hard": 24, "extreme": 17}
        keep = levels.get(difficulty, 30)
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        clues = self.size * self.size
        for (r, c) in cells:
            if clues <= keep: break
            backup = grid[r][c]
            grid[r][c] = 0
            if not self._has_unique_solution(deepcopy(grid)):
                grid[r][c] = backup
            else:
                clues -= 1
        return grid
