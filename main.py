import flask
import json
import logging

app = flask.Flask(__name__)


def next_coord(coord, board, move):
    if move == "up":
        if coord[1] - 1 < 0:
            return None
        return (coord[0], coord[1] - 1)
    elif move == "left":
        if coord[0] - 1 < 0:
            return None
        return (coord[0] - 1, coord[1])
    elif move == "right":
        if coord[0] + 1 > len(board[coord[0]]):
            return None
        return (coord[0] + 1, coord[1])
    elif move == "down":
        if coord[1] + 1 > len(board[coord[0]]):
            return None
        return (coord[0], coord[1] + 1)


def is_safe(board, coord):
    return board[coord[0]][coord[1]] is None


def do_move(state):
    width = state["board"]["width"]
    height = state["board"]["height"]
    board = [[None for _ in range(height)] for _ in range(width)]

    for coord in state["board"]["food"]:
        board[coord["x"]][coord["y"]] = "food"

    for snake in state["board"]["snakes"]:
        for coord in snake["body"]:
            board[coord["x"]][coord["y"]] = "snake"

    head = state["you"]["body"][0]
    me = (head["x"], head["y"])

    moves = ["up", "down", "left", "right"]
    for move in moves:
        target = next_coord(me, board, move)
        print(move, target)
        if target and is_safe(board, target):
            return move


@app.route("/")
def index():
    return "Hello"


@app.route("/start", methods=["GET", "POST"])
def start():
    return "Hello"


@app.route("/move", methods=["GET", "POST"])
def move():
    move = do_move(flask.request.json)
    return json.dumps({"move": move})


@app.route("/")
def hello():
    return "Get out of here John!"


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
