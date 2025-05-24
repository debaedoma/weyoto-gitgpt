from extensions import db
from datetime import datetime, timedelta
import secrets

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(db.String, unique=True, nullable=False, default=lambda: secrets.token_hex(16))
    github_pat = db.Column(db.String, nullable=True)
    request_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verification_code = db.Column(db.String, nullable=True)
    code_expires_at = db.Column(db.DateTime, nullable=True)
    last_code_sent_at = db.Column(db.DateTime, nullable=True)
    github_token = db.Column(db.String, nullable=True)
    is_pro = db.Column(db.Boolean, default=False)
    plan_type = db.Column(db.String)  # 'monthly' or 'annual'
    plan_expires_at = db.Column(db.DateTime)


class RequestLog(db.Model):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    endpoint = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
