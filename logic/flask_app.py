from flask import Flask, render_template, Response, request
from flask_sse import sse
import time
import json
from config.config import AppConfig


app = Flask(__name__, static_folder='../frontend/static',
            template_folder='../frontend/templates')
app.register_blueprint(sse, url_prefix="/stream")  # Initialize SSE extension
latest_message = None  # Variable to store the latest message


@app.route("/")
def index():
    """
    Renders the index.html template.

    Returns:
        str: The rendered index.html template.
    """
    return render_template("index.html")


@app.route("/stream/sse")
def stream():
    """
    This function is a Flask route that returns a server-sent event (SSE) stream.
    It continuously generates SSE messages containing the latest message data.

    Returns:
        Response: A Flask Response object with the SSE stream.

    """
    def generate():
        while True:
            if latest_message:
                # Write the latest message data directly to SSE stream
                yield f'data: {latest_message}\n\n'
            time.sleep(0.1)  # Sleep for a short while to prevent busy looping

    return Response(generate(), mimetype="text/event-stream")


@app.route("/stream/push", methods=["POST"])
def push():
    """
    Pushes a message to the server's event stream.

    This function is used to handle POST requests to the "/stream/push" endpoint. It expects a JSON payload containing a message. The function updates the global variable 'latest_message' with the JSON representation of the message.
    

    Returns:
        A tuple containing the string "OK" and the HTTP status code 200.

    Example:
        If a POST request is made to "/stream/push" with the following JSON payload:
        {
            "message": "Hello, world!"
        }
        The 'latest_message' variable will be updated with '{"message": "Hello, world!"}' and the function will return ("OK", 200).
    """
    global latest_message
    message = request.json
    latest_message = json.dumps(message)  # Update the latest message variable
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=AppConfig.DEBUG, host=AppConfig.HOST, port=AppConfig.PORT)
