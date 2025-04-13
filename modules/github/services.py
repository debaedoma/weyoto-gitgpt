import requests

def fetch_file_from_github(repo: str, file_path: str, token: str):
    """
    Fetch a specific file from a GitHub repo (raw content).
    """
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")


def list_repo_files(repo: str, token: str):
    """
    List all file paths in a repo by reading its tree.
    """
    url = f"https://api.github.com/repos/{repo}/git/trees/HEAD?recursive=1"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")


def get_latest_commit_info(repo: str, token: str):
    """
    Get the latest commit message, author, and date for a repo.
    """
    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        latest = response.json()[0]
        return {
            "message": latest["commit"]["message"],
            "author": latest["commit"]["author"]["name"],
            "timestamp": latest["commit"]["author"]["date"]
        }
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")


def list_user_repos(token: str):
    """
    List all repositories accessible to the authenticated user.
    """
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [repo["full_name"] for repo in data]
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
