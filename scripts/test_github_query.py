import requests

# Local URL where your Flask app is running
url = "http://127.0.0.1:5000/query/github/"

# JSON body you're sending to the API
data = {
    "repo": "https://github.com/yourname/yourrepo",
    "question": "What does this repo do?"
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
