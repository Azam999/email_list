import json

def get_emails_count(file):
    with open(file, 'r') as f:
        data = json.load(f)
        keys = data.keys()
        
        repo_emails = {}
        
        for key in keys:
            repo_emails[key] = len(data[key])
        
    return repo_emails


print(get_emails_count('data.json'))