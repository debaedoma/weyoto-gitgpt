from extensions import db
import datetime
import secrets

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(db.String, unique=True, nullable=False, default=lambda: secrets.token_hex(16))
    github_pat = db.Column(db.String, nullable=True)
    request_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
