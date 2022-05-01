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

    email_list = []
    for email in emails.find():
        email_list.append(email)
    
    return email_list

print(get_data('microsoft/typescript'))

# data = [
#     {
#         "number": 1,
#         "username": "w",
#         "email": "x"
#     },
#     {
#         "number": 2,
#         "username": "y",
#         "email": "z"
#     }]

# insert_data("microsoft/typescript", data)