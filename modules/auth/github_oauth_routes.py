from flask import Blueprint, redirect, request, jsonify
from models.user import User
from extensions import db
from config import Config
import requests
from middleware.auth import require_api_key
import os
from utils.encryption import encrypt_token
from flask_cors import cross_origin

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

# GitHub OAuth callback route — receives code and redirects to frontend
@github_oauth_bp.route("/github/oauth/callback")
def github_oauth_callback():
    # Extract the temporary authorization code from GitHub
    code = request.args.get("code")
    if not code:
        return jsonify({ "error": "Missing code" }), 400

    # Redirect to your frontend callback handler, passing the code
    # e.g. https://frontend.weyoto.com/github-callback?code=abc123
    frontend_callback_url = f"{Config.FRONTEND_BASE_URL}/github-callback?code={code}"
    return redirect(frontend_callback_url)


# Securely exchange GitHub OAuth code for access token and save it for the authenticated user
@github_oauth_bp.route("/github/oauth/save-token-from-code", methods=["POST"])
@cross_origin()
@require_api_key
def save_token_from_code():
    # Parse the GitHub 'code' from frontend's POST request
    code = request.json.get("code")
    if not code:
        return jsonify({ "error": "Missing code" }), 400

    # Exchange the code for a GitHub access token
    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code
        },
        headers={ "Accept": "application/json" }
    )

    # Parse the access token from GitHub's response
    token_json = token_resp.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return jsonify({ "error": "Token exchange failed", "details": token_json }), 400

    # Save the token to the currently authenticated user (from x-api-key)
    user = request.user
    user.github_token = encrypt_token(access_token)
    db.session.commit()

    return jsonify({ "message": "GitHub connected and token saved successfully for your account." })

@github_oauth_bp.route("/disconnect-github", methods=["POST"])
@require_api_key
def disconnect_github():
    user = request.user
    user.github_pat = None
    user.github_token = None
    db.session.commit()
    return jsonify({ "message": "GitHub connection removed successfully." })
