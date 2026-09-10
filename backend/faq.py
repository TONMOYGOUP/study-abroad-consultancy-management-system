from flask import Blueprint, jsonify

from database import get_all_faqs

faq = Blueprint("faq", __name__)


@faq.route("/api/faqs", methods=["GET"])
def get_faqs():
    try:
        faqs = [dict(row) for row in get_all_faqs()]
        return jsonify({
            "success": True,
            "faqs": faqs
        })
    except Exception as exc:
        print("FAQ ERROR:", repr(exc))
        return jsonify({
            "success": False,
            "message": "Unable to retrieve FAQs."
        }), 500
