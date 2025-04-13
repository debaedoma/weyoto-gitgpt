import requests

url = "http://127.0.0.1:5000/query/github"

repo = input("📁 Enter your GitHub repo (e.g., user/repo): ")
action = input("⚙️ Choose action (fetch_file, list_files, get_latest_commit): ").strip()

data = {
    "action": action,
    "repo": repo
}

if action == "fetch_file":
    data["path"] = input("📄 Enter file path (e.g., README.md): ")

headers = {
    "Content-Type": "application/json",
    "x-api-key": input("🔐 Enter your API key: ").strip()
}

response = requests.post(url, json=data, headers=headers)

print("\n--- RESPONSE ---")
print("Status Code:", response.status_code)
try:
    print("Body:", response.json())
except Exception:
    print("Raw:", response.text)
