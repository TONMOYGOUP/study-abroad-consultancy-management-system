from flask import Blueprint, request, jsonify

from database import get_connection, save_contact
from email_service import send_contact_notification

contact = Blueprint("contact", __name__)


@contact.route("/api/contact", methods=["POST"])
def create_contact():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Invalid request."}), 400

        full_name = data.get("full_name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        destination = data.get("destination", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        if not full_name or not email or not message:
            return jsonify({
                "success": False,
                "message": "Full name, email and message are required."
            }), 400

        contact_id = save_contact(
            full_name, email, phone, destination, subject, message
        )

        email_status = send_contact_notification(
            contact_id, full_name, email, phone,
            destination, subject, message
        )

        return jsonify({
            "success": True,
            "message": "Your message has been saved successfully!",
            "contact_id": contact_id,
            "email_status": email_status
        })

    except Exception as exc:
        print("CONTACT ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to save your message."
        }), 500


@contact.route("/api/contacts", methods=["GET"])
def get_contacts():
    try:
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

        return jsonify({"success": True, "contacts": contacts})

    except Exception as exc:
        print("GET CONTACTS ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to retrieve contacts."
        }), 500
