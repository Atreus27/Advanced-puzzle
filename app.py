from flask import Flask, render_template, jsonify, request
from puzzles.sudoku import generate_sudoku, solve_sudoku
from puzzles.fifteen import shuffle_board, move_tile
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# --- Health Check Routes (for Kubernetes & ALB) ---
@app.route('/health')
@app.route('/readyz')
@app.route('/livez')
def health():
    """
    Simple health check endpoints for Kubernetes and AWS ALB.
    Returns 200 OK when app is healthy.
    """
    return jsonify(status="ok", message="Sudoku service healthy"), 200


# --- Home route ---
@app.route('/')
def index():
    return render_template('index.html')


# --- Sudoku routes ---
@app.route('/sudoku')
def sudoku_page():
    board = generate_sudoku(40)  # 40 clues removed → medium-hard puzzle
    return render_template('sudoku.html', board=board)


@app.route('/api/sudoku/generate')
def api_sudoku_generate():
    clues = int(request.args.get('clues', 40))
    board = generate_sudoku(clues)
    return jsonify(board)


@app.route('/api/sudoku/solve', methods=['POST'])
def api_sudoku_solve():
    data = request.get_json()
    board = data.get('board')
    solved = solve_sudoku(board)
    return jsonify({'solved': solved})


# --- 15-Puzzle routes ---
@app.route('/fifteen')
def fifteen_page():
    board = shuffle_board()
    return render_template('fifteen.html', board=board)


@app.route('/api/fifteen/shuffle')
def api_fifteen_shuffle():
    return jsonify(shuffle_board())


@app.route('/api/fifteen/move', methods=['POST'])
def api_fifteen_move():
    data = request.get_json()
    board = data['board']
    tile = int(data['tile'])
    new_board = move_tile(board, tile)
    return jsonify(new_board)


# --- Entry point ---
if __name__ == '__main__':
    # Debug flag comes from config, controlled via environment
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
