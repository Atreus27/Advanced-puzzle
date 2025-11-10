from app.puzzles.sudoku import Sudoku

def test_generate_and_solve():
    s = Sudoku()
    grid = s.generate('easy')
    assert len(grid) == 9
    sol = s.solve([row[:] for row in grid])
    assert sol is not None
    for row in sol:
        assert set(row) == set(range(1, 10))
