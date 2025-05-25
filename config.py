import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("WEYOTO_GITGPT_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY_HEADER = "x-api-key"
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "noreply@notifications.weyoto.com")
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    ENABLE_GITHUB_OAUTH = os.getenv("ENABLE_GITHUB_OAUTH", "false").lower() == "true"
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL") #frontend callback URL for GitHub OAuth
    FREE_PLAN_LIMIT = int(os.getenv("FREE_PLAN_LIMIT", 20))
    FREE_PLAN_WINDOW_HOURS = int(os.getenv("FREE_PLAN_WINDOW_HOURS", 6))
