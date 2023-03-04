#__author__ = "Sascha Bharath"
#__version__ = "1.4"
#__project__ = "CS261 Group Project"
#__status__ = "Integration"

################### GIT TRACKING ###################

import requests
import json
import sqlalchemy
import sqlite3

## global variable for the GitHub access token
#token = ""

def count_commits(username, repository):
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


def git_progress(projectid, timeframe):
    ## get the username and repo name here using a sql query on the project id?
    #####################################################
    current_commits = count_commits(username, repository)

    ## obtain the sum of all he commits to the project so far
    commits_query = "SELECT numberOfCommits FROM gitTable WHERE gitTable.projectid=projectid;"
    commits = 0 #db.execute(commits_query, projectid=projectid).fetchall()
    
    ## obtain the number of commit readings we have done
    count_query = "SELECT COUNT(*) FROM gitTable WHERE gitTable.projectid=projectid;"
    count = 0 #db.execute(count_query, projectid=projectid).fetchall()
    
    ## get the number of commits from the last recording
    previous_commits_query = "SELECT numberOfCommits FROM gitTable WHERE gitTable.projectid=projectid AND timeframe=timeframe-1;"

    ## calculate average number of git commits for the project
    average_commits = sum(commits)/count

    ## very low number of commits so return a low score
    if (current_commits < 5) and (timeframe > 2):
        return 3
    ## below average so return a low score
    elif current_commits < average_commits:
        return 3
    ##  average so return a middle score
    elif current_commits==average_commits:
        return 5
    ## above average so return a high score
    elif (current_commits>average_commits) or (current_commits>= previous_commits*2)
        ## significant increase in commits so return highest score
        if current_commits>= previous_commits*2:
            return 10
        else:
            return 7
    else:
        return 5

#count_commits("5aschaB", "DummyRepo2", token)
