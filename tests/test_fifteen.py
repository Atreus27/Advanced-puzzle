from puzzles.fifteen import shuffle_board, move_tile


def test_shuffle_solvable_and_move():
    b = shuffle_board(10)
    flat = [c for row in b for c in row]
    assert 0 in flat

    # try to move a neighboring tile
    zi = flat.index(0)
    r, c = divmod(zi, 4)
    neighbors = []
    if r > 0: neighbors.append(b[r-1][c])
    if r < 3: neighbors.append(b[r+1][c])
    if c > 0: neighbors.append(b[r][c-1])
    if c < 3: neighbors.append(b[r][c+1])

    tile = neighbors[0]
    new = move_tile(b, tile)
    assert new != b