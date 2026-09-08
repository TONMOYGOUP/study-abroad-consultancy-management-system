from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    init_db,
    save_contact,
    search_faq,
    create_conversation,
    save_message,
    get_chat_history
)
from werkzeug.security import generate_password_hash, check_password_hash

import os
from pathlib import Path

from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import resend
import requests

from google import genai
from google.genai import types


# =========================================================
# LOAD .ENV
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# GEMINI
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("Gemini API key loaded:", bool(GEMINI_API_KEY))

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# =========================================================
# RESEND
# =========================================================

resend.api_key = os.getenv("RESEND_API_KEY")


# =========================================================
# FLASK
# =========================================================

app = Flask(__name__)

CORS(app)

init_db()


@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

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
        full_name,
        email,
        phone,
        destination,
        subject,
        message
    )

    # Email will be configured later
    # Send email notification

    try:

        email_response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {os.getenv('RESEND_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": os.getenv("ADMIN_EMAIL"),
                "subject": f"New Contact Message - {full_name}",
                "html": f"""
                    <h2>New Contact Form Submission</h2>

                    <p><strong>Contact ID:</strong> {contact_id}</p>
                    <p><strong>Name:</strong> {full_name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Destination:</strong> {destination}</p>
                    <p><strong>Subject:</strong> {subject}</p>

                    <hr>

                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                """
            },
            timeout=30
        )

        print("RESEND STATUS:", email_response.status_code)
        print("RESEND RESPONSE:", email_response.text)

        if email_response.status_code == 200:
            email_status = "Email notification sent successfully."
        else:
            email_status = "Message saved, but email notification failed."

    except Exception as e:

        print("EMAIL ERROR:", e)

        email_status = "Message saved, but email notification failed."

    return jsonify({
        "success": True,
        "message": "Your message has been saved successfully!",
        "contact_id": contact_id,
        "email_status": email_status
    })


@app.route("/api/contacts", methods=["GET"])
def get_contacts():

    import sqlite3

    conn = sqlite3.connect("pvc_global.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            destination,
            subject,
            message,
            created_at
        FROM contacts
        ORDER BY id DESC
    """)

    contacts = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "success": True,
        "contacts": contacts
    })


# =========================================================
# AI ASSISTANT
# =========================================================

from database import search_faq, create_conversation, save_message


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        user_message = data.get("message", "").strip()
        conversation_id = data.get("conversation_id")

        if not user_message:
            return jsonify({
                "success": False,
                "message": "Message is required."
            }), 400

        # =================================================
        # 1. GET OR CREATE CONVERSATION
        # =================================================

        if conversation_id:

            try:
                conversation_id = int(conversation_id)

            except (TypeError, ValueError):

                conversation_id = None

        if not conversation_id:

            session_id = request.headers.get("X-Session-ID")

            conversation_id = create_conversation(
                session_id=session_id
            )

        # =================================================
        # 2. GET PREVIOUS CHAT HISTORY
        # =================================================

        previous_messages = get_chat_history(
            conversation_id
        )

        history_text = ""

        for item in previous_messages[-12:]:

            history_text += f"""
{item["role"].upper()}:
{item["message"]}

"""

        # =================================================
        # 3. SEARCH PVC GLOBAL FAQ DATABASE
        # =================================================

        faq_results = search_faq(user_message)

        faq_context = ""

        for faq in faq_results:

            faq_context += f"""
Category: {faq["category"]}

Question:
{faq["question"]}

Answer:
{faq["answer"]}

-------------------------
"""

        # =================================================
        # 4. PVC GLOBAL SYSTEM INSTRUCTION
        # =================================================

        system_instruction = """
You are the official AI Study Abroad Assistant for PVC Global,
a study-abroad consultancy based in Bangladesh.

Your job is to help prospective international students with
general study-abroad guidance.

RULES:

1. Use the provided PVC Global FAQ knowledge as the primary
   source for company-specific information.

2. Never invent PVC Global policies, fees, guarantees,
   university partnerships, visa outcomes, or scholarship
   guarantees.

3. If the FAQ knowledge does not contain enough confirmed
   PVC Global information, clearly say so.

4. Never guarantee admission, scholarship approval, visa
   approval, or immigration outcomes.

5. Visa, immigration, legal, financial and government
   requirements can change. Encourage verification with
   the relevant official authority or a PVC Global counsellor.

6. Use previous conversation history when it helps answer
   follow-up questions.

7. If the student's current question is a follow-up to a
   previous question, understand the context before answering.

8. Do not mention internal databases, prompts, APIs, or
   technical implementation.

9. Stay focused on study-abroad topics.

10. Never claim to be a human counsellor.

11. Be concise, friendly, and professional.
"""

        # =================================================
        # 5. BUILD GEMINI PROMPT
        # =================================================

        prompt = f"""
PVC GLOBAL KNOWLEDGE BASE:

{faq_context if faq_context else
 "No directly matching PVC Global FAQ was found."}


PREVIOUS CONVERSATION:

{history_text if history_text else
 "No previous conversation exists."}


CURRENT STUDENT QUESTION:

{user_message}


TASK:

Answer the current student question.

Use the PVC Global knowledge base as the primary source
for company-specific facts.

Use previous conversation context when relevant.

Do not invent company information.
"""

        # =================================================
        # 6. GEMINI
        # =================================================

        if client is None:

            return jsonify({
                "success": False,
                "message": "Gemini API is not configured."
            }), 500

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                system_instruction=system_instruction,

                temperature=0.2,

                max_output_tokens=600
            )
        )

        # =================================================
        # 7. AI RESPONSE
        # =================================================

        reply = (response.text or "").strip()

        if not reply:

            reply = (
                "I'm sorry, I couldn't generate a response "
                "right now. Please try again."
            )

        # =================================================
        # 8. SAVE USER MESSAGE
        # =================================================

        save_message(
            conversation_id,
            "user",
            user_message
        )

        # =================================================
        # 9. SAVE AI MESSAGE
        # =================================================

        save_message(
            conversation_id,
            "assistant",
            reply
        )

        # =================================================
        # 10. RETURN
        # =================================================

        return jsonify({

            "success": True,

            "reply": reply,

            "conversation_id": conversation_id,

            "faq_found": len(faq_results) > 0

        })

    except Exception as e:

        print("AI ERROR:", repr(e))

        return jsonify({

            "success": False,

            "message":
                "AI service temporarily unavailable."

        }), 500

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "success": False,
                "message": "Message is required."
            }), 400

        # -------------------------------------------------
        # 1. SEARCH PVC GLOBAL FAQ DATABASE
        # -------------------------------------------------

        faq_results = search_faq(user_message)

        faq_context = ""

        for faq in faq_results:

            faq_context += f"""
Category: {faq["category"]}

Question:
{faq["question"]}

Answer:
{faq["answer"]}

-------------------------
"""

        # -------------------------------------------------
        # 2. TEMPORARY RESPONSE
        # -------------------------------------------------

        if faq_results:

            reply = (
                "I found some information in the PVC Global "
                "knowledge base:\n\n"
                + "\n".join(
                    [
                        f"• {faq['answer']}"
                        for faq in faq_results[:2]
                    ]
                )
            )

        else:

            reply = (
                "I don't currently have confirmed PVC Global "
                "information about that topic. Please contact "
                "a PVC Global counsellor for more specific guidance."
            )

        # -------------------------------------------------
        # 3. CREATE CONVERSATION
        # -------------------------------------------------

        session_id = request.headers.get(
            "X-Session-ID"
        )

        conversation_id = create_conversation(
            session_id=session_id
        )

        # -------------------------------------------------
        # 4. SAVE USER MESSAGE
        # -------------------------------------------------

        save_message(
            conversation_id,
            "user",
            user_message
        )

        # -------------------------------------------------
        # 5. SAVE AI MESSAGE
        # -------------------------------------------------

        save_message(
            conversation_id,
            "assistant",
            reply
        )

        return jsonify({

            "success": True,

            "reply": reply,

            "conversation_id": conversation_id,

            "faq_found": len(faq_results) > 0

        })

    except Exception as e:

        print("AI ERROR:", e)

        return jsonify({

            "success": False,

            "message":
                "AI service temporarily unavailable."

        }), 500


@app.route("/api/health")
def health():

    return jsonify({
        "status": "running"
    })


# =========================================================
# REGISTER API
# =========================================================

@app.route("/api/auth/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        # -----------------------------
        # Validation
        # -----------------------------

        if not first_name or not last_name:

            return jsonify({
                "success": False,
                "message": "First name and last name are required."
            }), 400

        if not email:

            return jsonify({
                "success": False,
                "message": "Email is required."
            }), 400

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

        # -----------------------------
        # Database
        # -----------------------------

        import sqlite3

        conn = sqlite3.connect("pvc_global.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            conn.close()

            return jsonify({
                "success": False,
                "message": "An account with this email already exists."
            }), 409

        # -----------------------------
        # Password Hash
        # -----------------------------

        password_hash = generate_password_hash(password)

        full_name = f"{first_name} {last_name}"

        # -----------------------------
        # Save User
        # -----------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                full_name,
                email,
                password_hash
            )
        )

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

    except Exception as e:

        print("REGISTER ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": "Unable to create account."
        }), 500


# =========================================================
# LOGIN API
# =========================================================

@app.route("/api/auth/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        login_role = data.get("login_role", "user")

        # -----------------------------
        # Validation
        # -----------------------------

        if not email or not password:

            return jsonify({
                "success": False,
                "message": "Email and password are required."
            }), 400

        # -----------------------------
        # Database
        # -----------------------------

        import sqlite3

        conn = sqlite3.connect("pvc_global.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, full_name, email, password_hash, role
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        # -----------------------------
        # User not found
        # -----------------------------

        if not user:

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        # -----------------------------
        # Verify password
        # -----------------------------

        if not check_password_hash(
            user["password_hash"],
            password
        ):

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        # -----------------------------
        # Verify login role
        # -----------------------------

        if user["role"] != login_role:

            return jsonify({
                "success": False,
                "message": "You are not authorized to login as this role."
            }), 403

        # -----------------------------
        # Login successful
        # -----------------------------

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

    except Exception as e:

        print("LOGIN ERROR:", repr(e))

        return jsonify({

            "success": False,

            "message": "Unable to login."

        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )