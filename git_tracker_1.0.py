#__author__ = "Sascha Bharath"
#__version__ = "1.0"
#__project__ = "CS261 Group Project"
#__status__ = "Production"

################### GIT TRACKING ###################
import requests

def count_commits(username, repository):

    # make a GET request to the GitHub API endpoint
    response = requests.get(f"https://api.github.com/repos/{username}/{repository}/commits")

    # if the request was successful
    if response.status_code == 200:
        # get the JSON data from the response
        data = response.json()

        # count the number of commits in the data
        commit_count = len(data)

        print(f"There are {commit_count} commits in the {username}/{repository} repository.")
    else:
        print("Failed to retrieve commit data.")

    return commit_count