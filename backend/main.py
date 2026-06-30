import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)


def _static_dir():
    """Resolve static folder for both dev (source tree) and frozen exe."""
    if getattr(sys, "frozen", False):
        # PyInstaller --onefile extracts to sys._MEIPASS
        return os.path.join(sys._MEIPASS, "frontend", "dist")
    return os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Python backend!", "time": __import__("datetime").datetime.now().isoformat()})


@app.route("/api/echo", methods=["POST"])
def echo():
    from flask import request
    return jsonify({"you_sent": request.get_json(silent=True) or {}})


# SPA fallback: serve built React for any unknown path
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    static = _static_dir()
    if path and os.path.exists(os.path.join(static, path)):
        return send_from_directory(static, path)
    return send_from_directory(static, "index.html")


def run_server(host="127.0.0.1", port=5000, debug=False):
    # use_reloader=False is required when running inside a thread/webview host
    app.run(host=host, port=port, debug=debug, use_reloader=False)


if __name__ == "__main__":
    run_server(debug=True)