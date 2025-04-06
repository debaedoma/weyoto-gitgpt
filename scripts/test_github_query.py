import requests

# Local URL where your Flask app is running
url = "http://127.0.0.1:5000/query/github/"

# JSON body you're sending to the API
data = {
    "action": "fetch_file",
    "repo": "octocat/hello-world",
    "path": "README.md"
}

# Optional headers – not needed unless your API requires keys
headers = {
    "Content-Type": "application/json"
}

# Send the request
response = requests.post(url, json=data, headers=headers)

# Print response details
print("Status Code:", response.status_code)
print("Response:", response.json())
