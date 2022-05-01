import requests
import os
from dotenv import load_dotenv

load_dotenv()

def requests_remaining():
    base_url = "https://api.github.com/users"
    request_headers = {'Authorization': f"token {os.getenv('GITHUB_TOKEN')}"}
    data = requests.get(base_url, headers=request_headers)
    total_requests_remaining = data.headers['X-RateLimit-Remaining'] + \
        "/" + data.headers['X-RateLimit-Limit']
    return total_requests_remaining
    
print(requests_remaining())