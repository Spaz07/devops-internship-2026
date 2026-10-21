import os
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1.0")
BROKEN = os.getenv("APP_BROKEN", "false").lower() == "true"


@app.route("/health")
def health():
    if BROKEN:
        return jsonify(status="unhealthy", version=VERSION), 500
    return jsonify(status="healthy", version=VERSION), 200


@app.route("/api/status")
def status():
    if BROKEN:
        return jsonify(status="error", version=VERSION), 500
    return jsonify(status="ok", version=VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
