import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("WEYOTO_GITGPT_DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY_HEADER = "x-api-key"
