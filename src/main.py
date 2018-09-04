import flask
import json

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Hello"


@app.route("/start", methods=["GET", "POST"])
def start():
    return "Hello"


@app.route("/move", methods=["GET", "POST"])
def move():
    return json.dumps({"move": "up"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
