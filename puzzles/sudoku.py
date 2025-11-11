import random
import copy

# Helper functions for Sudoku generation and solving


def pattern(r, c):
    """Define Sudoku pattern for a baseline valid board."""
    return (3 * (r % 3) + r // 3 + c) % 9


def shuffle(s):
    """Return a shuffled copy of a sequence."""
    s = list(s)
    random.shuffle(s)
    return s


def generate_full_board():
    """Generate a fully filled valid Sudoku board."""
    base = range(9)
    rows = [g * 3 + r for g in shuffle(range(3)) for r in shuffle(range(3))]
    cols = [g * 3 + c for g in shuffle(range(3)) for c in shuffle(range(3))]
    nums = shuffle(range(1, 10))
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board


# --- Solver (backtracking) ---


def find_empty(board):
    """Find the next empty cell (marked 0)."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def valid(board, row, col, val):
    """Check if placing val at (row, col) is valid."""
    if any(board[row][c] == val for c in range(9)):
        return False
    if any(board[r][col] == val for r in range(9)):
        return False
    br = row - row % 3
    bc = col - col % 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == val:
                return False
    return True


def solve_sudoku(board):
    """Solve the Sudoku board using backtracking."""
    b = copy.deepcopy(board)
    pos = find_empty(b)
    if not pos:
        return b
    r, c = pos
    for val in range(1, 10):
        if valid(b, r, c, val):
            b[r][c] = val
            solved = solve_sudoku(b)
            if solved:
                return solved
    return None


# --- Generator (remove clues) ---


def generate_sudoku(clues=40):
    """
    Generate a Sudoku puzzle by removing cells from a full valid board.
    `clues` = number of visible numbers (higher = easier)
    """
    full = generate_full_board()
    board = [row[:] for row in full]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    remove = 81 - clues
    for i in range(remove):
        r, c = cells[i]
        board[r][c] = 0
    return board