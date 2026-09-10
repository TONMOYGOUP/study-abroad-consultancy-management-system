from flask import Blueprint, jsonify

from database import get_connection

admin = Blueprint("admin", __name__)


@admin.route("/api/admin/contacts", methods=["GET"])
def admin_contacts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, email, phone, destination,
               subject, message, created_at
        FROM contacts
        ORDER BY id DESC
    """)

    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        "success": True,
        "contacts": contacts
    })
