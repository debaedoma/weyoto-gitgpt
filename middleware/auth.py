from flask import request, jsonify
from functools import wraps
from models.user import User
from extensions import db
from config import Config

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get(Config.API_KEY_HEADER)

        if not api_key:
            return jsonify({
                "error": "Missing API key.",
                "instructions": "Please include your x-api-key in the request headers."
            }), 401

        user = User.query.filter_by(api_key=api_key).first()

        if not user:
            return jsonify({
                "error": "Invalid API key.",
                "instructions": "Visit Weyoto GitGPT to get your personal key."
            }), 403

        # Attach user to the request context (optional for now)
        request.user = user
        return f(*args, **kwargs)
    return decorated
