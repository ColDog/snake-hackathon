import flask
import json
import logging
import os

app = flask.Flask(__name__)


def distance(coordA, coordB):
    x = coordA[0] - coordB[0]
    y = coordA[1] - coordB[1]
    return abs(x) + abs(y)


def closest_food(state, head):
    """
    returns coords to the nearest food, or None if there is ... none
    """
    foods = state["board"]["food"]
    if not len(foods):
        return None

    closest = None
    for food in state["board"]["food"]:
        food_coord = (food["x"], food["y"])
        if closest is None:
            closest = food_coord
            continue

        if distance(food_coord, head) < distance(closest, head):
            closest = food_coord
            continue
    return closest


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
        if coord[0] + 1 >= len(board[coord[0]]):
            return None
        return (coord[0] + 1, coord[1])
    elif move == "down":
        if coord[1] + 1 >= len(board[coord[0]]):
            return None
        return (coord[0], coord[1] + 1)


def is_safe(board, coord):
    return board[coord[0]][coord[1]] != "snake"


def is_dead(snake, board):
    if snake["health"] == 0:
        return True
    for coord in snake["body"]:
        if coord["x"] < 0:
            return True
        elif coord["y"] < 0:
            return True
        elif coord["x"] >= len(board):
            return True
        elif coord["y"] >= len(board[0]):
            return True


def do_move(state):
    width = state["board"]["width"]
    height = state["board"]["height"]
    board = [[None for _ in range(height)] for _ in range(width)]

    for coord in state["board"]["food"]:
        board[coord["x"]][coord["y"]] = "food"

    for snake in state["board"]["snakes"]:
        if is_dead(snake, board):
            continue
        for coord in snake["body"]:
            board[coord["x"]][coord["y"]] = "snake"

    head_coord = state["you"]["body"][0]
    tail_coord = state["you"]["body"][-1]
    me = (head_coord["x"], head_coord["y"])
    tail = (tail_coord["x"], tail_coord["y"])

    # Chase food
    def go_towards(destination):
        if (destination[0] - me[0]) < 0:
            target = next_coord(me, board, "left")
            if target and is_safe(board, target):
                return "left"
        if (destination[0] - me[0]) > 0:
            target = next_coord(me, board, "right")
            if target and is_safe(board, target):
                return "right"
        if (destination[1] - me[1]) < 0:
            target = next_coord(me, board, "up")
            if target and is_safe(board, target):
                return "up"
        if (destination[1] - me[1]) > 0:
            target = next_coord(me, board, "down")
            if target and is_safe(board, target):
                return "down"

    food_to_get = closest_food(state, me)

    if state["you"]["health"] < 20:
        food_to_get_dir = go_towards(food_to_get)
        if food_to_get_dir:
            return food_to_get_dir

    tail_dir = go_towards(tail)
    if tail_dir:
        return tail_dir

    # Default
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
    port = os.environ.get("PORT", "8080")
    app.run(host="0.0.0.0", port=int(port), debug=True)
