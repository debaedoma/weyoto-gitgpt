from flask import Blueprint, request, jsonify
from config import Config
from models.user import User
from datetime import datetime, timedelta

billing_bp = Blueprint("billing_bp", __name__)

@billing_bp.route("/activate", methods=["POST"])
def activate_paid_user():
    # Step 1: Get the user's API key from headers
    api_key = request.headers.get(Config.API_KEY_HEADER)

    # Step 2: Look up the user
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({ "error": "Invalid API key" }), 403

    # Step 3: Get the plan type from the request body
    data = request.get_json()
    plan = data.get("plan")

    # Step 4: Check that the plan is valid
    if plan not in ["monthly", "annual"]:
        return jsonify({ "error": "Invalid plan type. Must be 'monthly' or 'annual'." }), 400

    # Step 5: Set how long the plan lasts
    duration_days = 30 if plan == "monthly" else 365
    user.is_pro = True
    user.plan_type = plan
    user.plan_expires_at = datetime.utcnow() + timedelta(days=duration_days)

    # Step 6: Save to the database
    from extensions import db
    db.session.commit()

    return jsonify({
        "status": "activated",
        "plan": plan,
        "expires_at": user.plan_expires_at.isoformat()
    })
