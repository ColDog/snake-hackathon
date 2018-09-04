import flask
import json
# import snake
# import util
import logging

app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'Hello'


@app.route('/start', methods=['GET', 'POST'])
def start():
    return 'Hello'


@app.route('/move', methods=['GET', 'POST'])
def move():
    return json.dumps({'move': 'up'})

@app.route('/')
def hello():
    return 'Hello World!'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
