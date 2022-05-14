import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables in current directory
load_dotenv()


def insert_data(repo_name, data):
    mongo_uri = os.getenv('MONGO_URI')

    client = MongoClient(mongo_uri)

    emails = client.emails[repo_name]

    emails.insert_many(data)


def get_data(repo_name):
    mongo_uri = os.getenv('MONGO_URI')

    client = MongoClient(mongo_uri)

    emails = client.emails[repo_name]
    
    email_list = list(emails.find())
    
    return {
        "list": email_list,
        "count": len(email_list)
    }

print(get_data('microsoft/typescript'))