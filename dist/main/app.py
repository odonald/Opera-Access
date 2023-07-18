from flask import Flask, render_template, Response, request
from flask_sse import sse
import time
import json
import socket

app = Flask(__name__)
app.register_blueprint(sse, url_prefix="/stream")  # Initialize SSE extension
latest_message = None  # Variable to store the latest message

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream/sse")
def stream():
    def generate():
        while True:
            if latest_message:
                yield f'data: {latest_message}\n\n'  # Write the latest message data directly to SSE stream
            time.sleep(0.1)  # Sleep for a short while to prevent busy looping

    return Response(generate(), mimetype="text/event-stream")

@app.route("/stream/push", methods=["POST"])
def push():
    global latest_message
    message = request.json
    latest_message = json.dumps(message)  # Update the latest message variable
    return "OK", 200

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())  # Get the IP address of the machine
    port = 3210  # Replace with your desired port number
    app.run(debug=True, host=host, port=port)
