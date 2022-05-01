from math import ceil, floor
from turtle import update
import requests
import os
from dotenv import load_dotenv
import json
from mongo import insert_data

# Load environment variables in current directory
load_dotenv()

base_url = "https://api.github.com/"  # base Github api url
base_users_url = base_url + 'users/'
base_repos_url = base_url + 'repos/'


def update_json_file(account_name, repo_name, file_name, new_data):
    # Get current JSON data
    with open(file_name, 'r') as f:
        current_data = json.load(f)

    key = f'{account_name}/{repo_name}'

    if key in current_data:
        repo_data = current_data[key]
        repo_data += new_data
        current_data[f'{account_name}/{repo_name}'] = repo_data

        with open(file_name, 'w') as f:
            json.dump(current_data, f, indent=4)
    else:
        repo_data = []
        repo_data += new_data
        current_data[f'{account_name}/{repo_name}'] = repo_data

        with open(file_name, 'w') as f:
            json.dump(current_data, f, indent=4)



def get_repo_stargazers(account_name, repo_name, count=0):
    url = base_repos_url + f'{account_name}/{repo_name}'

    # Authorization headers for 5000 requests per hour
    request_headers = {'Authorization': f"token {os.getenv('GITHUB_TOKEN')}"}

    repo_info = requests.get(url, headers=request_headers)

    total_requests_remaining = repo_info.headers['X-RateLimit-Remaining'] + \
        "/" + repo_info.headers['X-RateLimit-Limit']
    print(total_requests_remaining)

    stargazers_count = repo_info.json()['stargazers_count']

    num_pages = 0
    page_start = 1
    start_index = 0

    if count > 0:
        page_start = floor(count / 100)
        start_index = round(((count / 100) % 1) * 100) - 1

        if (stargazers_count / 100) > 400:
            num_pages = 400
        else:
            num_pages = ceil(stargazers_count / 100)
    else:
        # Github pagination limit is < 401
        if (stargazers_count / 100) > 400:
            num_pages = 400
        else:
            num_pages = ceil(stargazers_count / 100)

    stargazers_url = url + '/stargazers?per_page=100'

    # 100 people per page to max number of pages, or 400 pages
    for i in range(page_start, num_pages + 1):
        stargazers_url = url + '/stargazers?per_page=100&page=' + str(i)
        stargazers_data = requests.get(stargazers_url, headers=request_headers)
        stargazers = stargazers_data.json()[start_index:99]

        email_list = []

        for stargazer in stargazers:
            count += 1
            username = stargazer['login']  # login is the Github username

            user_repos = requests.get(
                f'{base_users_url}{username}/repos', headers=request_headers)

            if len(user_repos.json()) > 0:
                # only non-forked repos
                try:
                    user_repo_name = next(user_repo for user_repo in user_repos.json(
                    ) if user_repo['fork'] == False)['name']
                except StopIteration:
                    continue

                user_repo_commits = requests.get(
                    f'{base_repos_url}{username}/{user_repo_name}/commits', headers=request_headers).json()

                if isinstance(user_repo_commits, list):
                    for user_repo_commit in user_repo_commits:
                        committer_username = user_repo_commit['url'].split(
                            '/')[4]
                        if (committer_username == username):
                            email = user_repo_commit['commit']['committer']['email']
                            
                            exclude_values = ["noreply", "macbook", "localhost", "gmail.com@", ".local", "github@"]
                            if any(exclude_value in email for exclude_value in exclude_values):
                                pass
                            else:
                                data = {
                                    "number": count,
                                    "username": username,
                                    "email": email
                                }

                                update_json_file(account_name, repo_name, 'info.json', [data])
                                
                                email_list.append(data)

                                print(f"{count}. {email}")
                            break  # skip to next stargazer
                else:
                    continue  # skip to next user if repo is empty
            else:
                continue  # skip to next user if the user has no repos
        
        insert_data(f'{account_name}/{repo_name}', email_list)
        email_list = []


# Get repositories list and create list
# with open('repositories.json', 'r') as f:
#     repositories_list = json.load(f)

get_repo_stargazers('microsoft', 'typescript', count=0)

# for repository in repositories_list:
#     get_repo_stargazers(repository['account_name'], repository['repo_name'], count=0)
