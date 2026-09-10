import os
import requests


def send_contact_notification(contact_id, full_name, email, phone,
                               destination, subject, message):
    api_key = os.getenv("RESEND_API_KEY")
    admin_email = os.getenv("ADMIN_EMAIL")

    if not api_key or not admin_email:
        return "Message saved, but email notification is not configured."

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": admin_email,
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

        print("RESEND STATUS:", response.status_code)
        print("RESEND RESPONSE:", response.text)

        if response.status_code == 200:
            return "Email notification sent successfully."

        return "Message saved, but email notification failed."

    except Exception as exc:
        print("EMAIL ERROR:", repr(exc))
        return "Message saved, but email notification failed."
