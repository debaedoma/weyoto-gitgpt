from flask import Blueprint, redirect, request, jsonify
from models.user import User
from extensions import db
from config import Config
import requests
from middleware.auth import require_api_key
import os

# Create a separate blueprint for GitHub OAuth routes
github_oauth_bp = Blueprint("github_oauth_bp", __name__)

# Start GitHub OAuth flow
@github_oauth_bp.route("/github/oauth/start")
def github_oauth_start():
    # Check if OAuth feature is enabled via config flag
    if not Config.ENABLE_GITHUB_OAUTH:
        return jsonify({"error": "OAuth disabled"}), 403

    # Redirect the user to GitHub's OAuth authorization screen
    client_id = Config.GITHUB_CLIENT_ID
    redirect_uri = Config.GITHUB_REDIRECT_URI
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=repo")

# Handle GitHub's redirect and exchange code for token
@github_oauth_bp.route("/github/oauth/callback")
def github_oauth_callback():
    # Check if OAuth is enabled
    if not Config.ENABLE_GITHUB_OAUTH:
        return jsonify({"error": "OAuth disabled"}), 403

    # Get the authorization code from GitHub's redirect
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing code from GitHub"}), 400

    # Exchange the code for an access token
    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code
        },
        headers={"Accept": "application/json"}
    )

    # Parse GitHub's token response
    token_json = token_resp.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return jsonify({"error": "Token exchange failed", "details": token_json}), 400

    # ✅ Do not save token here — user is unknown
    return jsonify({
        "access_token": access_token,
        "message": "Token retrieved. Now send it to /github-auth/github/oauth/save-token with your x-api-key."
    })

# Save GitHub token securely for authenticated user
@github_oauth_bp.route("/github/oauth/save-token", methods=["POST"])
@require_api_key
def save_oauth_token():
    # Use x-api-key authenticated user
    user = request.user
    data = request.get_json()
    token = data.get("access_token")

    if not token:
        return jsonify({ "error": "Missing access token." }), 400

    # Save the token to the user's record
    user.github_token = token
    db.session.commit()

    return jsonify({ "message": "GitHub connected and token saved successfully for your account." })

