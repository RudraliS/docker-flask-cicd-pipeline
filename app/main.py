from flask import Flask, jsonify, render_template
import os
import socket
from datetime import datetime, timezone

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("APP_ENV", "production")

@app.route("/")
def home():
    server_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    hostname = socket.gethostname()
    return render_template(
        "index.html",
        version=APP_VERSION,
        environment=ENVIRONMENT,
        hostname=hostname,
        server_time=server_time
    )

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/api/info")
def info():
    return jsonify({
        "app_name": "Dockerized Flask CI/CD Demo",
        "description": "Lightweight containerized Python service deployed with GitHub Actions",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "runtime": "Python 3.11 / Gunicorn"
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
