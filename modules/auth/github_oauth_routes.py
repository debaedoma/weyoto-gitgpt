from flask import Blueprint, redirect, request, jsonify
from models.user import User
from extensions import db
from config import Config
import requests
from middleware.auth import require_api_key

github_oauth_bp = Blueprint("github_oauth_bp", __name__)

@github_oauth_bp.route("/github/oauth/start")
def github_oauth_start():
    if not Config.ENABLE_GITHUB_OAUTH:
        return jsonify({"error": "OAuth disabled"}), 403

    client_id = Config.GITHUB_CLIENT_ID
    redirect_uri = Config.GITHUB_REDIRECT_URI
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=repo")

@github_oauth_bp.route("/github/oauth/callback")
def github_oauth_callback():
    if not Config.ENABLE_GITHUB_OAUTH:
        return jsonify({"error": "OAuth disabled"}), 403

    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing code from GitHub"}), 400

    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code
        },
        headers={"Accept": "application/json"}
    )

    token_json = token_resp.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return jsonify({"error": "Token exchange failed", "details": token_json}), 400

    return jsonify({
        "access_token": access_token,
        "message": "Token retrieved. Now send it to /auth/github/oauth/save-token with your x-api-key."
    })

@github_oauth_bp.route("/github/oauth/save-token", methods=["POST"])
@require_api_key
def save_oauth_token():
    user = request.user
    data = request.get_json()
    token = data.get("access_token")

    if not token:
        return jsonify({ "error": "Missing access token." }), 400

    user.github_token = token
    db.session.commit()

    return jsonify({ "message": "GitHub connected and token saved successfully for your account." })

