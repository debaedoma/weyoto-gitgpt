import requests

def list_repo_files(repo: str, token: str):
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
