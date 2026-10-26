from flask import Flask, jsonify
import os
import time

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/api/items", methods=["GET"])
def items():
    return jsonify(items=[
        {"id": 1, "name": "Item One"},
        {"id": 2, "name": "Item Two"},
        {"id": 3, "name": "Item Three"},
    ])


@app.route("/api/data", methods=["POST"])
def data():
    delay = float(os.getenv("API_DELAY", "0"))

    if delay > 0:
        time.sleep(delay)

    return jsonify(
        version=os.getenv("APP_VERSION", "1.0"),
        message="Performance testing API",
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
