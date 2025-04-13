from flask import Blueprint, request, jsonify
from extensions import db
from middleware.auth import require_api_key
from modules.github.services import (
    fetch_file_from_github,
    list_repo_files,
    get_latest_commit_info
)

github_bp = Blueprint("github_bp", __name__)

@github_bp.route("/", methods=["POST"])
@require_api_key
def query_github():
    data = request.get_json() or {}

    action = data.get("action")
    repo = data.get("repo")
    file_path = data.get("path", "README.md")
    question = data.get("question")

    if not repo:
        return jsonify({"error": "Missing 'repo' field."}), 400

    user = request.user
    if not user.github_pat:
        return jsonify({"error": "GitHub token not found."}), 403

    try:
        if action == "fetch_file":
            content = fetch_file_from_github(repo, file_path, user.github_pat)
            if content is None:
                return jsonify({"error": f"File '{file_path}' not found in '{repo}'."}), 404
            return jsonify({
                "status": "ok",
                "action": "fetch_file",
                "repo": repo,
                "file_path": file_path,
                "content": content[:2000],
                "question": question
            })

        elif action == "list_files":
            files = list_repo_files(repo, user.github_pat)
            if files is None:
                return jsonify({"error": f"Repo '{repo}' not found."}), 404
            return jsonify({
                "status": "ok",
                "action": "list_files",
                "repo": repo,
                "files": files[:500]  # Trim for now
            })

        elif action == "get_latest_commit":
            commit = get_latest_commit_info(repo, user.github_pat)
            if commit is None:
                return jsonify({"error": f"Repo '{repo}' not found."}), 404
            return jsonify({
                "status": "ok",
                "action": "get_latest_commit",
                "repo": repo,
                "latest_commit": commit
            })

        else:
            return jsonify({"error": "Invalid or missing action."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

