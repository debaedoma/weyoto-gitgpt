import requests
from config import Config

def send_verification_email(to_email: str, code: str):
    payload = {
        "from": Config.EMAIL_SENDER,
        "to": [to_email],
        "subject": "Your Weyoto GitGPT Verification Code",
        "html": f"<p>Your login code is <strong>{code}</strong>. It expires in 30 minutes.</p>"
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {Config.RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print("📬 Resend response status:", response.status_code)
    print("📬 Resend response body:", response.text)
    return response
