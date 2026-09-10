from flask import Blueprint, request, jsonify

from database import (
    search_faq,
    create_conversation,
    save_message,
    get_chat_history,
)
from gemini_service import generate_ai_response

ai_assistant = Blueprint("ai_assistant", __name__)


# =========================================================
# AI CHAT
# =========================================================

@ai_assistant.route("/api/ai/chat", methods=["POST"])
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
        session_id = request.headers.get("X-Session-ID")

        if not user_message:
            return jsonify({
                "success": False,
                "message": "Message is required."
            }), 400

        # -------------------------------------------------
        # Validate conversation ID
        # -------------------------------------------------

        if conversation_id:
            try:
                conversation_id = int(conversation_id)
            except (TypeError, ValueError):
                conversation_id = None

        # -------------------------------------------------
        # Create new conversation if needed
        # -------------------------------------------------

        if not conversation_id:
            conversation_id = create_conversation(
                session_id=session_id
            )

        # -------------------------------------------------
        # Get previous messages
        # -------------------------------------------------

        previous_messages = get_chat_history(
            conversation_id
        )

        # -------------------------------------------------
        # Search FAQ knowledge base
        # -------------------------------------------------

        faq_results = search_faq(
            user_message
        )

        # -------------------------------------------------
        # Generate AI response
        # -------------------------------------------------

        reply = generate_ai_response(
            user_message=user_message,
            previous_messages=previous_messages,
            faq_results=faq_results,
        )

        # -------------------------------------------------
        # Save USER message
        # -------------------------------------------------

        save_message(
            conversation_id,
            "user",
            user_message
        )

        # -------------------------------------------------
        # Save AI message
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
            "faq_found": len(faq_results) > 0,
        })

    except Exception as exc:

        print("AI ERROR:", repr(exc))

        return jsonify({
            "success": False,
            "message": "AI service temporarily unavailable."
        }), 500


# =========================================================
# GET CHAT HISTORY
# =========================================================

@ai_assistant.route(
    "/api/ai/history/<int:conversation_id>",
    methods=["GET"]
)
def ai_history(conversation_id):

    try:

        messages = get_chat_history(
            conversation_id
        )

        history = []

        for message in messages:

            history.append({
                "role": message["role"],
                "message": message["message"],
                "created_at": message["created_at"]
            })

        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "messages": history
        })

    except Exception as exc:

        print("HISTORY ERROR:", repr(exc))

        return jsonify({
            "success": False,
            "message": "Unable to load chat history."
        }), 500

    #for load history

    @ai_assistant.route("/api/ai/history/<int:conversation_id>", methods=["GET"])
def ai_history(conversation_id):
    try:
        messages = get_chat_history(conversation_id)

        history = []

        for message in messages:
            history.append({
                "role": message["role"],
                "message": message["message"],
                "created_at": message["created_at"]
            })

        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "messages": history
        })

    except Exception as exc:
        print("HISTORY ERROR:", repr(exc))

        return jsonify({
            "success": False,
            "message": "Unable to load chat history."
        }), 500