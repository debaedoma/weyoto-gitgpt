import os
import requests
from flask import Flask, jsonify, request
import base64  # Required to decode file content from GitHub

# Initialize Flask app
app = Flask(__name__)

# Load API key from system environment
API_KEY = os.getenv("WEYSENTINEL_API_KEY")

# GitHub Credentials
GITHUB_TOKEN = os.getenv("WEYSENTINEL_GITHUB_PAT")
REPO_OWNER = "debaedoma"
REPO_NAME = "wey-sentinel"

# Common headers for GitHub API
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


# Function to fetch latest commits
def get_latest_commits():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch commits: {response.status_code}"}


# Function to fetch file content from GitHub
def get_file_content(file_path):
    """
    Fetches the raw content of a file from GitHub.
    :param file_path: The file path in the repo (e.g., "requirements.txt")
    :return: JSON response with the file content (decoded)
    """
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        if "content" in file_data:
            decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
            return {"file_name": file_data["name"], "content": decoded_content}
        else:
            return {"error": "File content not found"}
    else:
        return {"error": f"Failed to fetch file: {response.status_code}"}


# Function to fetch file structure (list of all files)
def get_file_tree(branch="main"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get("tree", [])
    else:
        return {"error": f"Failed to fetch file tree: {response.status_code}"}


# Route to fetch latest commits
@app.route('/get-latest-code', methods=['GET'])
def fetch_code():
    provided_key = request.headers.get("X-API-KEY")
    if not provided_key or provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    commits = get_latest_commits()
    return jsonify(commits)


# Route to fetch file content
@app.route('/get-file-content', methods=['GET'])
def fetch_file():
    provided_key = request.headers.get("X-API-KEY")
    if not provided_key or provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    file_path = request.args.get("path")
    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    file_content = get_file_content(file_path)
    return jsonify(file_content)


# Route to list all files and folders
@app.route('/list-files', methods=['GET'])
def list_files():
    provided_key = request.headers.get("X-API-KEY")
    if not provided_key or provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    file_tree = get_file_tree()
    return jsonify(file_tree)


# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
