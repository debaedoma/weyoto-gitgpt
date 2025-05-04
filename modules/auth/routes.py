from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from services.email import send_verification_email
from datetime import datetime, timedelta
import random
import secrets
from middleware.auth import require_api_key


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/request-code", methods=["POST"])
def request_code():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)

    # Cooldown check (60 seconds)
    if user.last_code_sent_at and (datetime.utcnow() - user.last_code_sent_at).total_seconds() < 60:
        return jsonify({
            "error": "Please wait before requesting another code.",
            "cooldown_seconds": 60
        }), 429

    code = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=30)

    user.verification_code = code
    user.code_expires_at = expiry
    user.last_code_sent_at = datetime.utcnow()  # 👈 Track timestamp

    db.session.add(user)
    db.session.commit()

    send_verification_email(email, code)

    return jsonify({ "message": f"Verification code sent to {email}." })

@auth_bp.route("/verify-code", methods=["POST"])
def verify_code():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    if not email or not code:
        return jsonify({"error": "Email and code are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or user.verification_code != code:
        return jsonify({"error": "Invalid code or user."}), 401

    if user.code_expires_at < datetime.utcnow():
        return jsonify({"error": "Code has expired."}), 401

    user.verification_code = None
    user.code_expires_at = None
    db.session.commit()

    return jsonify({
        "message": "Verification successful.",
        "api_key": user.api_key
    })

@auth_bp.route("/view-api-key", methods=["GET"])
@require_api_key
def get_api_key():
    user = request.user
    return jsonify({
        "email": user.email,
        "api_key": user.api_key
    })

@auth_bp.route("/regenerate-api-key", methods=["POST"])
@require_api_key
def regenerate_api_key():
    user = request.user
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({ "error": "Verification code is required." }), 400

    if user.verification_code != code or user.code_expires_at < datetime.utcnow():
        return jsonify({ "error": "Invalid or expired verification code." }), 401

    # Invalidate code after use
    user.verification_code = None
    user.code_expires_at = None

    # Generate new key
    new_key = secrets.token_hex(16)
    user.api_key = new_key
    db.session.commit()

    return jsonify({
        "message": "API key regenerated successfully.",
        "api_key": new_key
    })
