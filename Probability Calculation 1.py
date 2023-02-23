### PROBABILITY CALCULATION ###



# Import modules #

from datetime import date
from math import floor
import numpy as np
import scipy.stats as st


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
zVals = [-0.84162, -0.38532, 0.12566, 0.67449, 1.28155] # Z-values associated with given fuzzy values

#put the elif blocks into separate functions
def fDeadline(deadline, values):
    if ((deadline - date.today()).days // 7) > 2:
        return values[4]
    elif ((deadline - date.today()).days // 7) < -2:
        return values[0]
    else:
        return values[((deadline - date.today()).days // 7) + 2]

def fBudget(used, expected, values):
    if used / expected >= 2.0:
        return values[4]
    elif (used / expected) <= 0.25:
        return values[0]
    else:
        return values[int(round((used / expected) * 2.0) / 2.0) + 1]

def fBugs(bugs, values):
    if (bugs // 3) == 0:
        return values[4]
    elif (bugs // 3) >= 4:
        return values[0]
    else:
        return values[4-(associatedBugs // 3)]

def fTeam(size, startSize, values):
    if (size / startSize) <= 0.6:
        return values[0]
    elif (size / startSize) >= 1.0:
        return values[4]
    else:
        return values[int((round((size / startSize), 1) - 0.6) * 10)]
    
def findZ(inputVal, values, zs): # finds z-value associated with inputVal
    for i in values:
        if inputVal == values[i]:
            z = zs[i]
        else:
            break
    return(z)

def mean(v1, deadline): #finds mean of a normal distribution for a metric
    coeff1 = (2.32635 / v1)
    coeff2 = (coeff1 * deadline) - (4 * deadline)
    mean = coeff2 / (coeff1 - 1)
    return(mean)

def standardDev(v1, deadline, mean):
    return((deadline - mean)/v1)

st.norm.cdf(deadline)

# Form normal distributions relating to each metric #

deadlineNormal = np.random.normal("", "", "")

# Reconcile metrics to form a final distribution #

# Output final distribution's weekly probability totals as an array of decimals # - Interfacing needed

def probabilityDict(deadline):
    dict = {}
    i=0
    while i <= (deadline*4):
        p = st.norm.cdf(i) - st.norm.cdf(i-1)
        dict[i] = p
    return(dict)