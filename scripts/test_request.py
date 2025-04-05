import requests

url = "http://localhost:5000/query/github"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "cb1552afc11d3a23b5e194245038a4c7"
}
data = {
    "repo": "octocat/hello-world",
    "question": "What’s in the README?"
}

res = requests.post(url, json=data, headers=headers)
print(res.status_code)
print(res.json())
