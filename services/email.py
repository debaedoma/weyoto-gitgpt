import requests
from config import Config

def send_verification_email(to_email: str, code: str):
    return requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {Config.RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "from": Config.EMAIL_SENDER,
            "to": [to_email],
            "subject": "Your Weyoto GitGPT Login Code",
            "html": f"<p>Your login code is <strong>{code}</strong>. It expires in 10 minutes.</p>"
        }
    )
