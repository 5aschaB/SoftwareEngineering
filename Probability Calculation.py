### PROBABILITY CALCULATION ###



# Import modules #

from datetime import date
from math import floor
import numpy as np


# Take inputs # - Interfacing and advice on data types needed

subprocessID = "" #int

# date vars currently taking dummy data #
startDate = date(2023, 1, 4)
subprocessDeadline = date(2023, 4, 10)
deadline = date(2023, 6, 20)
currentDate = date.today()

# budget vars currently taking dummy data #
totalBudget = 10000
budgetUsed = 5000

# associatedBugs currently taking dummy data #
associatedBugs = 4

# teamSize vars currently taking dummy data #
startingTeamSize = 6
teamSize = 5

teamMorale = "" #int

teamWellbeing = "" #int

absences = "" #int



# Compare input values with expected value given subprocess state #

# subprocessDelta = (subprocessDeadline - currentDate).days # days from now to subprocess deadline
projectDelta = (deadline - currentDate).days # days from now to project deadline

expectedBudget = (totalBudget / (deadline - startDate).days) * (date.today() - startDate).days




# Apply fuzzy logic to form probability of on-time completion #

fuzzyVals = [0.2, 0.35, 0.55, 0.75, 0.9]

#put the elif blocks into separate functions
def fDeadline(subprocessDeadline, fuzzyVals):
if ((subprocessDeadline - date.today()).days // 7) > 2:
    return fuzzyVals[4]
elif ((subprocessDeadline - date.today()).days // 7) < -2:
    return fuzzyVals[0]
else:
    return fuzzyVals[((subprocessDeadline - date.today()).days // 7) + 2]

def fBudget(budgetUsed, expectedBudget, fuzzyVals)
if budgetUsed / expectedBudget >= 2.0:
    return fuzzyVals[4]
elif (budgetUsed / expectedBudget) <= 0.25:
    return fuzzyVals[0]
else:
    return fuzzyVals[int(round((budgetUsed / expectedBudget) * 2.0) / 2.0) + 1]

def fBugs(associatedBugs, fuzzyVals)
if (associatedBugs // 3) == 0:
    return fuzzyVals[4]
elif (associatedBugs // 3) >= 4:
    return fuzzyVals[0]
else:
    return fuzzyVals[4-(associatedBugs // 3)]

def fTeam(teamSize, startingTeamSize, fuzzyVals)
if (teamSize / startingTeamSize) <= 0.6:
    return fuzzyVals[0]
elif (teamSize / startingTeamSize) >= 1.0:
    return fuzzyVals[4]
else:
    return fuzzyVals[int((round((teamSize / startingTeamSize), 1) - 0.6) * 10)]

# Form normal distributions relating to each metric #

deadlineNormal = np.random.normal("", "", sz)

# Reconcile metrics to form a final distribution #

# Output final distribution's weekly probability totals as an array of decimals # - Interfacing needed
