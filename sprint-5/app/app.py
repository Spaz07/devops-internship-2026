
import os
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "unknown")
HEALTHY = os.getenv("APP_HEALTHY", "true").lower() == "true"


@app.route("/")
def home():
    return jsonify(
        application="Sprint 5 Blue-Green Demo",
        version=VERSION,
        status="running"
    )


@app.route("/healthz")
def health():
    if not HEALTHY:
        return jsonify(status="unhealthy"), 503

    return jsonify(status="healthy", version=VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
