import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def requests_remaining():
    base_url = "https://api.github.com/users"
    request_headers = {'Authorization': f"token {os.getenv('GITHUB_TOKEN')}"}
    data = requests.get(base_url, headers=request_headers)
    total_requests_remaining = data.headers['X-RateLimit-Remaining'] + \
        "/" + data.headers['X-RateLimit-Limit']
    return total_requests_remaining

def email_count():
    with open('test.json') as f:
        data = json.load(f)
    data = data['microsoft/typescript']
    return len(data)

print(email_count())
print(requests_remaining())