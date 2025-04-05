import requests

def fetch_file_from_github(repo: str, file_path: str, token: str):
    """
    Fetch a specific file from a public or private GitHub repo.
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
