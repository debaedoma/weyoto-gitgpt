from flask import Blueprint, request, jsonify
from extensions import db
from middleware.auth import require_api_key
from models.user import User
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
    data = request.get_json()

    action = data.get("action")
    repo = data.get("repo")
    file_path = data.get("path")

    if not action:
        return jsonify({"error": "Missing action field."}), 400

    try:
        if action == "fetch_file":
            if not repo or not file_path:
                return jsonify({"error": "Missing repo or path for fetch_file."}), 400

            content = fetch_file_from_github(repo, file_path, user.github_pat)
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

            files = list_repo_files(repo, user.github_pat)
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

            commit = get_latest_commit_info(repo, user.github_pat)
            if commit is None:
                return jsonify({"error": "Could not fetch commit."}), 404

            return jsonify({
                "status": "ok",
                "action": action,
                "repo": repo,
                "commit": commit
            })

        elif action == "list_user_repos":
            repos = list_user_repos(user.github_pat)
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
        return jsonify({"error": "Missing GitHub token."}), 400

    user.github_pat = token
    db.session.commit()

    return jsonify({"message": "GitHub token saved."})
