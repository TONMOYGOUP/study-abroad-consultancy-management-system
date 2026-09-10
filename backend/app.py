from flask import Flask, jsonify
from flask_cors import CORS

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

app.register_blueprint(auth)
app.register_blueprint(contact)
app.register_blueprint(ai_assistant)
app.register_blueprint(admin)
app.register_blueprint(faq)
app.register_blueprint(dashboard)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
