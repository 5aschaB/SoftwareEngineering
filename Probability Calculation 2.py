### PROBABILITY CALCULATION ###



# Import modules #

from datetime import date
from math import floor, sqrt
import numpy as np
import scipy.stats as st

# Take inputs # - Interfacing and advice on data types needed

subprocessID = "" #int

fuzzyPercentiles = [0.2, 0.35, 0.55, 0.75, 0.9] # fuzzy logic scores needed to create later functions


# date vars currently taking dummy data #
startDate = date(2023, 1, 4)
subprocessDeadline = date(2023, 4, 10)
projectDeadline = date(2023, 6, 20)
currentDate = date.today()

# budget vars currently taking dummy data #
totalBudget = 10000
budgetUsed = 5000

# associatedBugs currently taking dummy data #
associatedBugs = 4

# teamSize vars currently taking dummy data #
startingTeamSize = 6
teamSize = 5

teamMorale = "" # int from 1-10

teamWellbeing = "" #int from 1-10

absences = "" #int detailing the number of days of absence for a given week

# weightings currently taking dummy data #
weightings = [3, 2, 1, 1, 0, 1, 0]
# generally weightings = [x, y, z, a, a, a, a] such that x relates to deadline, y to budget, z to bugs and a to soft metrics
# x, y, z are ints from 1 to 3, a is an int from 0 to 3
combinedWeighting = sum(weightings)

# Compare input values with expected value given subprocess state #

# subprocessDelta = (subprocessDeadline - currentDate).days # days from now to subprocess deadline
projectDelta = (projectDeadline - currentDate).days # days from now to project deadline

expectedBudget = (totalBudget / (projectDeadline - startDate).days) * (date.today() - startDate).days

# Apply fuzzy logic to form probability of on-time completion #

fuzzyPercentiles = [0.2, 0.35, 0.55, 0.75, 0.9]

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

def fTeamSize(size, startSize, values):
    if (size / startSize) <= 0.6:
        return values[0]
    elif (size / startSize) >= 1.0:
        return values[4]
    else:
        return values[int((round((size / startSize), 1) - 0.6) * 10)]

def fMoraleWellbeing(metric, values): # serves as the fuzzy value generator for teamMorale and teamWellbeing
    try:
        return values[metric//2]
    except:
        print("Metric value out of range")
        return(0)

def fAbsences(metric, teamMembers, values): # assumes a 5-day working week for all team members
    max = teamMembers / 5
    if (metric == 0):
        return values[4]
    elif (metric / max) >= 0.15:
        return values[0]
    else:
        return values[((metric / max)// 0.05) + 1]
    
def rawValueToZ(rawValue, mean, sd): # finds z-value associated with a raw value, given the standard deviation and mean, to 5 d.p.
    z = round(((rawValue - mean) / sd), 5)
    return(z)

def mean(value, deadline): #finds mean of a normal distribution for a metric
    z = round(st.norm.ppf(value), 5) # finds z-value of value to 5 d.p.
    coeff1 = (2.32635 / z)
    coeff2 = (coeff1 * deadline) - (4 * deadline)
    mean = coeff2 / (coeff1 - 1)
    return(mean)

def standardDev(value, deadline, mean):
    return((deadline - mean)/(round(st.norm.ppf(value), 5)))

# Form normal distributions relating to each metric #

deadlineStats, budgetStats, bugStats, teamSizeStats, teamMoraleStats, teamWellbeingStats, absenceStats = []

metricSummaryStats = []

# i hate how this bit looks too but its important and works, I'll change it later when im commenting everything up. probably. i want to change how this looks
count = 0
for i in weightings:
    if i == 0:
        weightings.remove(i)
    else:
        if count == 0:
            deadlineStats = [mean(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline), standardDev(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline, mean(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline))]
            metricSummaryStats.append(deadlineStats)
        elif count == 1:
            budgetStats = [mean(fBudget(budgetUsed, expectedBudget, fuzzyPercentiles), subprocessDeadline), standardDev(fBudget(budgetUsed, expectedBudget, fuzzyPercentiles), subprocessDeadline, mean(fBudget(budgetUsed, expectedBudget, fuzzyPercentiles)))]
            metricSummaryStats.append(budgetStats)
        elif count == 2:
            bugStats = [mean(fBugs(associatedBugs, fuzzyPercentiles), subprocessDeadline), standardDev(fBugs(associatedBugs, fuzzyPercentiles), subprocessDeadline, mean(fBugs(associatedBugs, fuzzyPercentiles), subprocessDeadline))]
            metricSummaryStats.append(bugStats)
        elif count == 3:
            teamSizeStats = [mean(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles), subprocessDeadline), standardDev(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles), subprocessDeadline, mean(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles)))]
            metricSummaryStats.append(teamSizeStats)
        elif count == 4:
            teamMoraleStats = [mean(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline))]
            metricSummaryStats.append(teamMoraleStats)
        elif count == 5:
            teamWellbeingStats = [mean(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline))]
            metricSummaryStats.append(teamWellbeingStats)
        elif count == 6:
            absenceStats = [mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline), standardDev(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline, mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline))]
            metricSummaryStats.append(absenceStats)
        else: break
    count += 1

# Reconcile metrics to form a final distribution #

reconciledMean, reconciledStandardDev = 0

def reconcileStats(m, sd, metricStats, weights, totalWeight):
    for i in len(metricStats):
        m += (weights[i] * (1/totalWeight) * metricStats[i][0])
        sd += (weights[i] * ((1/totalWeight)**2) * (metricStats[i][1]**2))
    sd = sqrt(sd)
    return([m, sd])

# Output final distribution's weekly probability totals as an array of decimals # - Interfacing needed

def probabilityDict(deadline, mean, sd):
    dict = {}
    for i in range((deadline*4)): # cut-off point for normal distribution will be
                                  # its expected deadline multiplied by 4
        
        z1 = rawValueToZ((i+1), mean, sd) # z-value of the week i+1
        z2 = rawValueToZ(i, mean, sd)     # z-value of the week i
        dict[int(i+1)] = (st.norm.cdf(z1) - st.norm.cdf(z2)) # dictionary element i+1 assigned to be
                                                             # left-tail probability of z-value of week i+1
                                                             # minus that of week i
                                                             # i.e. week 1 probability = cumulative probability at week 1 - cumulative probability at week 0
    return(dict)