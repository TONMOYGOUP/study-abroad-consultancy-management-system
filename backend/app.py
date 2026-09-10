from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path

from database import init_db
from auth import auth
from contact import contact
from ai_assistant import ai_assistant
from admin import admin
from faq import faq
from dashboard import dashboard

app = Flask(__name__)
CORS(app)

init_db()

# Register existing API blueprints
app.register_blueprint(auth)
app.register_blueprint(contact)
app.register_blueprint(ai_assistant)
app.register_blueprint(admin)
app.register_blueprint(faq)
app.register_blueprint(dashboard)


# =========================
# Frontend
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# =========================
# Health Check
# =========================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)