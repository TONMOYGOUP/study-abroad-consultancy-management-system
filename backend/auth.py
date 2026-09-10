from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection

auth = Blueprint("auth", __name__)


@auth.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Invalid request."}), 400

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        if not first_name or not last_name:
            return jsonify({
                "success": False,
                "message": "First name and last name are required."
            }), 400

        if not email:
            return jsonify({"success": False, "message": "Email is required."}), 400

        if password != confirm_password:
            return jsonify({
                "success": False,
                "message": "Passwords do not match."
            }), 400

        if len(password) < 8:
            return jsonify({
                "success": False,
                "message": "Password must be at least 8 characters."
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({
                "success": False,
                "message": "An account with this email already exists."
            }), 409

        password_hash = generate_password_hash(password)
        full_name = f"{first_name} {last_name}"

        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (full_name, email, password_hash, "user"))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Account created successfully.",
            "user": {
                "id": user_id,
                "full_name": full_name,
                "email": email,
                "role": "user"
            }
        }), 201

    except Exception as exc:
        print("REGISTER ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to create account."
        }), 500


@auth.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Invalid request."}), 400

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        login_role = data.get("login_role", "user")

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required."
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, email, password_hash, role
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        if user["role"] != login_role:
            return jsonify({
                "success": False,
                "message": "You are not authorized to login as this role."
            }), 403

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    except Exception as exc:
        print("LOGIN ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to login."
        }), 500
