from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from services.email import send_verification_email
from datetime import datetime, timedelta
import random

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/request-code", methods=["POST"])
def request_code():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required."}), 400

    code = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=10)

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)

    user.verification_code = code
    user.code_expires_at = expiry

    db.session.add(user)
    db.session.commit()

    send_verification_email(email, code)

    return jsonify({"message": f"Verification code sent to {email}."})


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
