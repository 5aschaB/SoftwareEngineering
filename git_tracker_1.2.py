#__author__ = "Sascha Bharath"
#__version__ = "1.2"
#__project__ = "CS261 Group Project"
#__status__ = "Production"

################### GIT TRACKING ###################

import requests
import json

def count_commits(username, repository, token):

    # set the headers to include the authentication token
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # make a GET request to the GitHub API endpoint
    response = requests.get(f"https://api.github.com/repos/{username}/{repository}/commits", headers=headers)

    # if the request was successful
    if response.status_code == 200:
        # get the JSON data from the response
        data = response.json()
        # count the number of commits in the data
        commit_count = len(data)
        print(f"There are {commit_count} commits in the {username}/{repository} repository.")
    
    else:
        try:
            print(response.json())
            ## check if the repo is empty
            if "Git Repository is empty" in response.json()["message"]:
                print("Git Repository is empty")
                commit_count = 0
            ## check if the repo does not exist
            elif response.status_code==404:
                print("Git Repository does not exist or permission denied")
                commit_count = -1           
            else:
                print("Failed to retrieve commit data. Status code: " + str(response.status_code))
                commit_count = -1
        except:
            print("Failed to retrieve commit data.")
            commit_count = -1

    return commit_count


# GitHub personal access token
token = ""

count_commits("5aschaB", "DummyRepo2", token)
