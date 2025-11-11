from puzzles.sudoku import generate_sudoku, solve_sudoku


def test_generate_and_solve():
    # Generate a sudoku with 30 clues (harder puzzle)
    board = generate_sudoku(30)
    assert len(board) == 9
    assert all(len(row) == 9 for row in board)

    # Solve the puzzle using backtracking
    solved = solve_sudoku(board)
    assert solved is not None

    # Each row must contain digits 1–9 exactly once
    for row in solved:
        assert sorted(row) == list(range(1, 10))

    # Each column must also contain digits 1–9
    for c in range(9):
        col = [solved[r][c] for r in range(9)]
        assert sorted(col) == list(range(1, 10))