from flask import Blueprint, request, jsonify
from middleware.auth import require_api_key
from modules.github.services import fetch_file_from_github

github_bp = Blueprint("github_bp", __name__)

@github_bp.route("/", methods=["POST"])
@require_api_key
def query_github():
    data = request.get_json() or {}
    repo = data.get("repo")
    file_path = data.get("path", "README.md")
    question = data.get("question")

    # Validate inputs
    if not repo:
        return jsonify({"error": "Missing 'repo' field."}), 400

    user = request.user
    if not user.github_pat:
        return jsonify({"error": "GitHub token not found. Please connect your account."}), 403

    try:
        content = fetch_file_from_github(repo, file_path, user.github_pat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if content is None:
        return jsonify({"error": f"File '{file_path}' not found in '{repo}'."}), 404

    return jsonify({
        "status": "ok",
        "source": "github",
        "repo": repo,
        "file_path": file_path,
        "content": content[:2000],  # Optional: truncate long files for GPT
        "question": question
    })
