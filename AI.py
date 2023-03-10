# @Sam Malcolm

#~#~# RECOMMENDATION AI #~#~#

# Import modules #

import random as r

# recommendation arrays will contain strings describing recommended actions to rectify issues which might be occurring
# these arrays will also become 2D, such that array[0] contains all recommendations relating to metrics[0], and so on

# Receive inputs from User and Risk Matrix #

# User interaction with chatbot will generate a specific metric for which they require guidance
# userInput will take the form metrics[x], such that the requested guidance metric is containe in userInput
# seriousness will take an integer score from 1 to 5 (aligning with the Risk Matrix scoring system)
                 # this will inform the later bias towards the given metric

# Reconcile user and risk matrix inputs with AI behaviour #

# Artificially Intelligent behaviour exhibited in so far as it can disagree with the user's selected area of failure,
# meaning that if the user requests advice on improving a metric which is not thought to be an issue by the risk matrix,
# the AI can somewhat redirect the user and offer recommendations more pertinent to the current state of project metrics
def recommend(priorities, userInput, seriousness, budget, alreadySpent, deadline, startDate, commits, wellbeing, morale, teamSize, startingTeamSize, absences):
    
    metrics = ["deadline", "budget", "commits", "teamSize", "morale", "wellbeing", "absences"]

    # recommendation arrays will contain strings describing recommended actions to rectify issues which might be occurring
    # these arrays will also become 2D, such that arr[0] contains all recommendations relating to metrics[0], and so on
    weakRecommendations = [["Call a team meeting to address deadline concerns", "Incentivise prompt completion of tasks", "Consider whether each team member is working to their strengths"],
                           ["Consider minor cutbacks of non-essential workplace items", "Notify management of your concerns", "Seek cheaper alternatives to office essentials"],
                           ["Ensure familiarity of tracking software across the team", "Seek to identify the root cause of the slow work pacing", "Consider whether each team member is working to their strengths"],
                           ["Prioritise the most critical parts of the team's work", "Communicate openly with the team about the challenges that a reduced team size will pose", "Consider re-allocating team members to best suit the needs of the team"],
                           ["Make sure that good work is being recognised and rewarded", "Address team concerns and conflicts in a prompt manner", "Seek to provide opportunities for personal growth and development in the work environment"],
                           ["Identify and address the root cause of the team's wellbeing issues", "Consider adjusting workload, or placing different team members on different tasks", "Be flexible in adjusting expectations to meet the team members' needs"],
                           ["Look to temporarily re-allocate work", "Ensure the impact of the absences is properly assessed", "Train team members in one another's responsibilities to ensure they are as well serviced as possible during absences"]]   # will be made when risk matrix indicates a lower level of concern for the user-specified metric
    
    strongRecommendations = [["Consider re-evaluating your deadline", "Seek a deadline extension", "Re-evaluate which components of the project must be implemented prior to the current deadline"],
                             ["Consider consulting a financial advisor", "Consult management for advice on alleviating budget concerns", "Consider reducing project scope"],
                             ["Consider re-evaluating how much work should have been done at this stage", "Consider alternative working arrangements, such as more collaborative development", "Provide regular feedback and be honest with team on how the project is progressing"],
                             ["Look to hire competent replacements", "Look to management to provide a temporary replacement", "Consider sending currrent team members on education courses to develop their skills"],
                             ["Consider the work-life balance of the team", "Try providing team social events during standard work hours", "Consider giving the team time off in order to come back refreshed"],
                             ["Consider giving the team time off work to overcome wellbeing issues", "Look into the possibility of counselling for either indivisual team members or the group", "Seek advice from a medical professional if necessary"],
                             ["Seek a temporary replacement for the absentee(s)", "Look to work remotely if the absentee(s) feel capable of doing so", "Look to outsource the absentee's workload for the duration of their absence"]] # will be made when risk matrix indicates a higher level of concern for the user-specified metric
    
    riskMatrix = [] # will be formed of the respective scores from 1 to 10 of each metric in metrics
    
    # prioArray will hold indexes of all metrics with priority greater than or equal to 3
    prioArray = []
    count = 0
    for i in priorities:
        if i >= 3:
            prioArray.append(count)
        count += 1
    prioArrElem = r.randint(0, len(prioArray)) # generates a random element in prioArray, this code is only ever called through once so this will effectiveley generate a new nuber each request
    recommendations = { #takes the form of a dictionary matching eventualities to specific outputs
        
        # first case, when the user's choice of metric has a level of concern >= 5 (out of 10), and user-defined seriousness is aligned with this (also >= 3)
        # outputs a random strong recommendation relating to the user's chosen metric
        (riskMatrix[metrics.index(userInput)] >= 5) & (seriousness >= 3) : (strongRecommendations[metrics.index(userInput)][r.randint(0, len(strongRecommendations[metrics.index(userInput)]))]),

        # second case, when the user's choice of metric has a level of concern >= 5, but user-defined seriousness is not aligned with this (< 3)
        # outputs a random strong recommendation relating to the user's chosen metric
        # outputs a random weak recommendation relating to the user's chosen metric
        (riskMatrix[metrics.index(userInput)] >= 5) & (seriousness < 3) : [(strongRecommendations[metrics.index(userInput)][r.randint(0, len(strongRecommendations[metrics.index(userInput)]))]),
                                                                            (weakRecommendations[metrics.index(userInput)][r.randint(0, len(weakRecommendations[metrics.index(userInput)]))])],
        
        # third case, when the user's choice of metric has a level of concern < 5, there is another metric with a level of concern >= 5 and the user has a seriousness score >= 3
        # outputs a random weak recommendation relating to the user's chosen metric
        # outputs a warning that there are more significant areas of concern detected
        # outputs a strong recommendation from another metric with area of concern >=3
        (riskMatrix[metrics.index(userInput)] < 5) & 
        (seriousness >= 3) &
        (len(prioArray) > 0) : 
        [(weakRecommendations[metrics.index(userInput)][r.randint(0, len(weakRecommendations[metrics.index(userInput)]))]),
        "Note: Other, more significant issues have been detected, an example of a recommendation to resolve such an issue will follow",
        strongRecommendations[prioArray[prioArrElem]][r.randnint(0, len(strongRecommendations[prioArray[prioArrElem]]))]],

        # fourth case, when the user's choice of metric has a level of concern < 5, there is another metric with a level of concern >= 5 and the user has a seriousness score < 3
        # outputs a warning that there are more significant areas of concern detected
        # outputs a strong recommendation from another metric with area of concern >=3
        (riskMatrix[metrics.index(userInput)] < 5) &
        (seriousness < 3) &
        (len(prioArray) > 0) :
        [["Note: Other, more significant issues have been detected, an example of a recommendation to resolve such an issue will follow"],
        strongRecommendations[prioArray[prioArrElem]][r.randnint(0, len(strongRecommendations[prioArray[prioArrElem]]))]],

        # fifth case, when the user's choice of metric has a level of concern < 5, there is no other metric with a level of concern >= 5 and the user has a seriousness score >= 3
        # outputs a random weak recommendation relating to the user's chosen metric 
        # outputs reassurance that there are no major issues detected by the risk matrix at this time
        (riskMatrix[metrics.index(userInput)] < 5) &
        (seriousness >= 3) &
        (len(prioArray) == 0) :
        [weakRecommendations[metrics.index(userInput)][r.randint(0, len(weakRecommendations[metrics.index(userInput)]))], 
        "Note: No significant issues have been detected in the project at this time"],

        # sixth case, when the user's choice of metric has a level of concern < 5, there is no other metric with a level of concern >= 5 and the user has a seriousness score < 3
        # outputs a random weak recommendation relating to the user's chosen metric 
        (riskMatrix[metrics.index(userInput)] < 5) &
        (seriousness < 3) &
        (len(prioArray == 0)):
        [weakRecommendations[metrics.index(userInput)][r.randint(0, len(weakRecommendations[metrics.index(userInput)]))]]
    }
    return (recommendations)

# Output recommendation(s) #