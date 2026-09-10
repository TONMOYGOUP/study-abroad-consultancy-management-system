from flask import Blueprint, jsonify

from database import get_connection

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/api/dashboard", methods=["GET"])
def dashboard_info():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()["total_users"]

        cursor.execute("SELECT COUNT(*) AS total_contacts FROM contacts")
        total_contacts = cursor.fetchone()["total_contacts"]

        cursor.execute("SELECT COUNT(*) AS total_conversations FROM conversations")
        total_conversations = cursor.fetchone()["total_conversations"]

        conn.close()

        return jsonify({
            "success": True,
            "dashboard": {
                "total_users": total_users,
                "total_contacts": total_contacts,
                "total_conversations": total_conversations
            }
        })

    except Exception as exc:
        print("DASHBOARD ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to load dashboard data."
        }), 500
