from flask import Blueprint, request, jsonify
from extensions import db
from middleware.auth import require_api_key
from models.user import User
from config import Config
from datetime import datetime, timedelta
from utils.billing import get_limit_and_logs, log_request
from utils.limits import generate_limit_response
from utils.encryption import encrypt_token, decrypt_token
from modules.github.services import (
    fetch_file_from_github,
    list_repo_files,
    get_latest_commit_info,
    list_user_repos
)

github_bp = Blueprint("github_bp", __name__)

@github_bp.route("/query", methods=["POST"])
@require_api_key
def query_github():
    user = request.user

    # 🔁 Step 1: Downgrade expired Pro users
    if user.is_pro and user.plan_expires_at and datetime.utcnow() > user.plan_expires_at:
        user.is_pro = False
        user.plan_type = None
        user.plan_expires_at = None
        db.session.commit()

    # 🚦 Step 2: If not Pro, check usage
    if not user.is_pro:
        logs, max_allowed = get_limit_and_logs(user.id)

        if len(logs) >= max_allowed:
            oldest = logs[0].created_at
            try_again_time = oldest + timedelta(hours=Config.FREE_PLAN_WINDOW_HOURS)
            return jsonify(generate_limit_response(try_again_time)), 403

    # 📝 Step 3: Log the request
    log_request(user.id, endpoint="/github/query")

    # 🧠 Continue with GitHub logic...
    data = request.get_json()

    raw_token = user.github_token or user.github_pat
    if raw_token:
        token = decrypt_token(raw_token)
    else:
        return jsonify({"error": "GitHub not connected. Please visit https://gitgpt.weyoto.com/dashboard to connect your GitHub codebase."}), 400

    action = data.get("action")
    repo = data.get("repo")
    file_path = data.get("path")

    if not action:
        return jsonify({"error": "Missing action field."}), 400

    try:
        if action == "fetch_file":
            if not repo or not file_path:
                return jsonify({"error": "Missing repo or path for fetch_file."}), 400

            content = fetch_file_from_github(repo, file_path, token)
            if content is None:
                return jsonify({"error": "File not found."}), 404

            return jsonify({
                "status": "ok",
                "action": action,
                "repo": repo,
                "path": file_path,
                "content": content
            })

        elif action == "list_files":
            if not repo:
                return jsonify({"error": "Missing repo for list_files."}), 400

            files = list_repo_files(repo, token)
            if files is None:
                return jsonify({"error": "Repo not found or empty."}), 404

            return jsonify({
                "status": "ok",
                "action": action,
                "repo": repo,
                "files": files
            })

        elif action == "get_latest_commit":
            if not repo:
                return jsonify({"error": "Missing repo for get_latest_commit."}), 400

            commit = get_latest_commit_info(repo, token)
            if commit is None:
                return jsonify({"error": "Could not fetch commit."}), 404

            return jsonify({
                "status": "ok",
                "action": action,
                "repo": repo,
                "commit": commit
            })

        elif action == "list_user_repos":
            repos = list_user_repos(token)
            if repos is None:
                return jsonify({"error": "Unable to retrieve repositories."}), 404

            return jsonify({
                "status": "ok",
                "action": action,
                "repos": repos
            })

        else:
            return jsonify({"error": f"Unsupported action: {action}"}), 400

    except Exception as e:
        return jsonify({"error": "GitHub request failed.", "details": str(e)}), 500


@github_bp.route("/set-pat", methods=["POST"])
@require_api_key
def set_pat():
    user = request.user
    data = request.get_json()
    token = data.get("github_pat")

    if not token:
        return jsonify({ "error": "Missing GitHub token." }), 400

    # 🔍 Try calling GitHub to validate token before saving
    try:
        test_repos = list_user_repos(token)
        if test_repos is None:
            raise ValueError("Invalid PAT")
    except Exception:
        return jsonify({ "error": "Invalid or expired GitHub token. Ensure you're inputting a valid fine-grained PAT" }), 401

    user.github_pat = encrypt_token(token)
    db.session.commit()

    return jsonify({ "message": "GitHub token saved successfully." })
