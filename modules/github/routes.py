from flask import Blueprint, request, jsonify
from middleware.auth import require_api_key

github_bp = Blueprint("github_bp", __name__)

@github_bp.route("/", methods=["POST"])
@require_api_key
def query_github():
    data = request.get_json() or {}
    repo = data.get("repo")
    question = data.get("question")

    return jsonify({
        "status": "ok",
        "source": "github",
        "repo": repo,
        "question": question
    })
