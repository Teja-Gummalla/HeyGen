import datetime
import random

# Flask imports
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

# processing time in seconds
PROCESSING_TIME = 5
status_context = {}


@app.route("/status")
def get_status():
    """
    The user iteracts with this endpoint to find the status
    of their video translation.

    input: no input
    Response(JSON):
    - status: (string) one of the following status values: pending, error, completed
    """
    current_time = datetime.datetime.now()
    status = 'pending'

    # for test scenarios
    if 'process_until' not in status_context:
        status_context['process_until'] = datetime.datetime.now() + datetime.timedelta(seconds=PROCESSING_TIME)

    if current_time >= status_context['process_until']:
        status = random.choices(['completed', 'error'], k=1)[0]

    return jsonify({
        "status": status,
    })

if __name__ == '__main__':
    status_context['process_until'] = datetime.datetime.now() + datetime.timedelta(seconds=PROCESSING_TIME)
    app.run(port=8080)