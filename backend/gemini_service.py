import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Gemini API key loaded:", bool(GEMINI_API_KEY))

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
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


def generate_ai_response(user_message, previous_messages, faq_results):
    if client is None:
        raise RuntimeError("Gemini API is not configured.")

    history_text = ""
    for item in previous_messages[-12:]:
        history_text += f"""
{item["role"].upper()}:
{item["message"]}

"""

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

    if not faq_context:
        faq_context = "No directly matching PVC Global FAQ was found."

    if not history_text:
        history_text = "No previous conversation exists."

    prompt = f"""
PVC GLOBAL KNOWLEDGE BASE:

{faq_context}


PREVIOUS CONVERSATION:

{history_text}


CURRENT STUDENT QUESTION:

{user_message}


TASK:

Answer the current student question.

Use the PVC Global knowledge base as the primary source
for company-specific facts.

Use previous conversation context when relevant.

Do not invent company information.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            max_output_tokens=600
        )
    )

    reply = (response.text or "").strip()
    if not reply:
        reply = "I'm sorry, I couldn't generate a response right now. Please try again."

    return reply
