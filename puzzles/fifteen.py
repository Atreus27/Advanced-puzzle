import random
import copy

# Target solved board (4x4 grid)
TARGET = [1, 2, 3, 4,
          5, 6, 7, 8,
          9, 10, 11, 12,
          13, 14, 15, 0]


def shuffle_board(moves=200):
    """
    Shuffle the 15-puzzle board by performing random legal moves.
    Ensures the board remains solvable.
    """
    board = TARGET[:]  # make a copy
    for _ in range(moves):
        zero = board.index(0)
        r, c = divmod(zero, 4)
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))
        if r < 3:
            neighbors.append((r + 1, c))
        if c > 0:
            neighbors.append((r, c - 1))
        if c < 3:
            neighbors.append((r, c + 1))
        nr, nc = random.choice(neighbors)
        ni = nr * 4 + nc
        board[zero], board[ni] = board[ni], board[zero]
    return [board[i * 4:(i + 1) * 4] for i in range(4)]


def move_tile(board, tile):
    """
    Move the selected tile into the empty space if the move is legal.
    Returns a new board state.
    """
    flat = [c for row in board for c in row]
    if tile not in flat or tile == 0:
        return board

    zi = flat.index(0)
    ti = flat.index(tile)
    zr, zc = divmod(zi, 4)
    tr, tc = divmod(ti, 4)

    # Check adjacency
    if abs(zr - tr) + abs(zc - tc) == 1:
        flat[zi], flat[ti] = flat[ti], flat[zi]

    # Return reshaped 4x4 grid
    return [flat[i * 4:(i + 1) * 4] for i in range(4)]