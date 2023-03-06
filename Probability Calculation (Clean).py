#~#~# PROBABILITY CALCULATION #~#~#

## IMPORT MODULES ##

from datetime import date, timedelta
from math import sqrt
import scipy.stats as st

## INITIALISE VARIABLES (will be params of function)##

# fuzzy logic scores associated with probability of punctual task completion

# contains state of risk matrix given as an array of values from 1-10
riskMatrix = []

# date variables, form subprocessDeadline from duration and startDate
startDate, projectDeadline, subprocessDeadline = 0 #start date of project, deadline of project, deadline of subprocess (only thing which is not a risk matrix (1-10) score)
# will take data type 'date' from datetime

# budget variables
totalBudget, budgetUsed = 0 # total project budget, budget used so far (

# commit variable
commits = 0 # score from risk matrix associated with git commits

# teamSize variables
startingTeamSize, teamSize = 0 # team size at the beginning of the project, team size at present

# team morale variable
teamMorale = 0 # integer value describing team morale at present

# team wellbeing variable
teamWellbeing = 0 # integer value describing team wellbeing at present

# absences variable
absences = 0 # number of days of absence in present working week

# summary statistic arrays
deadlineStats, budgetStats, bugStats, teamSizeStats, teamMoraleStats, teamWellbeingStats, absenceStats, metricSummaryStats, weightings = []
# the above arrays named (metric)Stats will store summary statistics pertaining to their named metric
# metricSummaryStats will become a 2D array, storing summary statistics of all metrics desired by the user
# weightings will store the respecive weightings of each metric, as set by the user

# INITIALISE FUNCTIONS #

def fDeadline(deadline, values): # takes subprocess deadline and fuzzy values as inputs
    if ((deadline - date.today()).days // 7) >= 2:               # if >= 14 days until deadline, output most positive fuzzy value
        return values[4]
    elif ((deadline - date.today()).days // 7) < -2:             # if >= 14 days beyond deadline, output least positive fuzzy value
        return values[0]
    else:
        return values[((deadline - date.today()).days // 7) + 2] # otherwise, output a fuzzy value in line with the expressed formula

def fBudget(used, total, values): # takes budget used, expected budget used and fuzzy values as its inputs
    if used / total >= 2.0:                                       # if more than double expected budget used, output least positive fuzzy value
        return values[0]
    elif (used / total) <= 0.25:                                  # if less that 1/4 expected budget used, output most positive fuzzy value
        return values[4]
    else:
        return values[int(round((used / total) * 2.0) / 2.0) + 1] # otherwise, output a fuzzy value in line with the expressed formula

# COMMITS NEEDS REWORKING, MATHS WILL MAKE SENSE SOON xxxx #
def fCommits(commits, values): # takes bugs associated with subprocess and fuzzy values as inputs
    if (commits // 3) == 0:             # if less that 3 bugs present, output most positive fuzzy value
        return values[4]
    elif (commits // 3) >= 4:           # if greater than 12 bugs present, output least positive fuzzy value
        return values[0]
    else:
        return values[4-(commits // 3)] # otherwise, output a fuzzy value in line with the expressed formula

def fTeamSize(size, startSize, values): # takes current team size, starting team size and fuzzy values as input
    if (size / startSize) <= 0.6:                                       # if current team size is equivalent to 60% or less of initial team size, output least positive fuzzy value
        return values[0]
    elif (size / startSize) >= 1.0:                                     # if current team size is greater than or equal to initial team size, output most positive fuzzy value
        return values[4]
    else:
        return values[int((round((size / startSize), 0.1) - 0.6) * 10)] # otherwise, output a fuzzy value in line with the expressed formula

def fMoraleWellbeing(metric, values): # serves as the fuzzy value generator for morale and wellbeing, taking either of those metrics as well as fuzzy values as input
    try:
        if (metric == 10): return values[4] # if metric score is 10 (maximum), output most positive fuzzy value
        else: return values[metric//2]      # otherwise, output a fuzzy value in line with the expressed formula
    except:
        print("Metric value out of range")  # if the prior code generates invalid input, then the zmetric data is unsuitable
        return(0)

def fAbsences(metric, teamMembers, values): # takes week's absences, current number of team mambers and fuzzy values as inputs
    maxAbsences = teamMembers * 5                          # assumption that the working week is 5 days long for each employee
    if (metric == 0):                                      # if there are no absences, return the most positive fuzzy value
        return values[4]
    elif (metric / maxAbsences) >= 0.15:                   # if greater than 15% of possible workdays are absences, return the least positive fuzzy value
        return values[0]
    else:
        return values[((metric / maxAbsences)// 0.05) + 1] # otherwise, output a fuzzy value in line with the expressed formula

def mean(value, deadline): #finds mean of a normal distribution for a metric, takes a fuzzy value and subprocess deadline as inputs
    z = round(st.norm.ppf(value), 5)              # finds z-value of value to 5 d.p.
    coeff1 = (-2.32635 / z)                       # -2.32635 is the z-value corresponding to the 1st percentile in the standard normal distribution
    coeff2 = (coeff1 * deadline)                  # formation of coefficients coeff1 and coeff2 explained in documentation
    return(coeff2 / (coeff1 - 1))                 # reasoning for this computing mean also explained in documentation

def standardDev(value, deadline, mean): # finds standard deviation of a normal distribution for a metric, takes fuzzy value, subprocess deadline and mean as inputs
    return((deadline - mean)/(round(st.norm.ppf(value), 5))) # reasoning for this computing standard deviation explained in documentation

def rawValueToZ(rawValue, mean, sd): # finds z-value associated with a raw value (i.e. time value along the x-axis of a normal distribution), given the standard deviation and mean, to 5 d.p.
    return(round(((rawValue - mean) / sd), 5)) # reasoning for this computing z-value explained in documentation

def reconcileStats(metricStats, weights): # reconciles summary statistics from multiple normal distributions, takes array of metric atats and array of weightings
    m, sd = 0                                                                 # initialises variables to hold mean and standard deviation
    for i in len(metricStats):
        m += (weights[i] * (1/(sum(weights))) * metricStats[i][0])            # adds weighted mean to m
        sd += (weights[i] * ((1/(sum(weights)))**2) * (metricStats[i][1]**2)) # adds weighted variance to sd
    sd = sqrt(sd)                                                             # finds square root of sd (weighted variances), result is weighted standard deviation
    return([m, sd])

def probabilityDict(deadline, mean, sd): # forms a dictionary of cumulative probabilities from week 0 to week (deadline * 4)
    dict = {}
    for i in range(9):                            # cut-off point for normal distribution will be 10 weeks        
        z1 = rawValueToZ((i+1), mean, sd)                    # z-value of the week i+1
        z2 = rawValueToZ(i, mean, sd)                        # z-value of the week i
        dict[int(i+1)] = (st.norm.cdf(z1) - st.norm.cdf(z2)) # dictionary element i+1 assigned to be
                                                             # left-tail probability of z-value of week i+1
                                                             # minus that of week i
                                                             # i.e. week 1 probability = cumulative probability at week 1 - cumulative probability at week 0
    return(dict)

# CODE BODY (functionify)#
def reconcileMetrics(startDate, projectDeadline, subprocessDuration, totalBudget, budgetUsed, commits, startingTeamSize, teamSize, morale, wellbeing, absences):
    fuzzyPercentiles = [0.35, 0.5, 0.65, 0.8, 0.95]
    subprocessDeadline = startDate + timedelta(days=(subprocessDuration * 7))
    count = 0
    for i in weightings: # considers each element of the weightings array
        if i == 0:
            weightings.remove(i) # if a metric at position x has no weighting, then it is not required by the user, thus it is removed from the weightings array
                                # count is later incremented, ensuring that the metric at position x is skipped over
                                # at this stage, the actual weighting is not considered, that comes later
        else:
                                # (metric)Stats is a 2-element array formed from the mean and standard deviation of its respective metric
                                # the function associated with each metric is used in mean and standard deviation calculations to give a fuzzy value
                                # if (metric)Stats is calculated then it is appended to metricSummaryStats
            if count == 0:       # weighting index 0 pertains to deadline metric
                deadlineStats = [mean(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline), standardDev(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline, mean(fDeadline(subprocessDeadline, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(deadlineStats)
            elif count == 1:     # weighting index 1 pertains to budget metric
                budgetStats = [mean(fBudget(budgetUsed, totalBudget, fuzzyPercentiles), subprocessDeadline), standardDev(fBudget(budgetUsed, totalBudget, fuzzyPercentiles), subprocessDeadline, mean(fBudget(budgetUsed, totalBudget, fuzzyPercentiles)))]
                metricSummaryStats.append(budgetStats)
            elif count == 2:     # weighting index 2 pertains to bug metric
                bugStats = [mean(fCommits(commits, fuzzyPercentiles), subprocessDeadline), standardDev(fCommits(commits, fuzzyPercentiles), subprocessDeadline, mean(fCommits(commits, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(bugStats)
            elif count == 3:     # weighting index 3 pertains to team size metric
                teamSizeStats = [mean(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles), subprocessDeadline), standardDev(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles), subprocessDeadline, mean(fTeamSize(teamSize, startingTeamSize, fuzzyPercentiles)))]
                metricSummaryStats.append(teamSizeStats)
            elif count == 4:     # weighting index 4 pertains to team morale metric
                teamMoraleStats = [mean(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(teamMorale, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(teamMoraleStats)
            elif count == 5:     # weighting index 5 pertains to team wellbeing metric
                teamWellbeingStats = [mean(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(teamWellbeing, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(teamWellbeingStats)
            elif count == 6:     # weighting index 6 pertains to absences metric
                absenceStats = [mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline), standardDev(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline, mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(absenceStats)
            else: break
        count += 1

    reconciledMean = reconcileStats(metricSummaryStats, weightings)[0]        # stores weighted mean of all desired metrics
    reconciledStandardDev = reconcileStats(metricSummaryStats, weightings)[1] # stores weighted standard deviation of all desired metrics

    probabilities = probabilityDict(subprocessDeadline, reconciledMean, reconciledStandardDev) # stores dictionary of cumulative probabilities as described in probabilityDict function

# Only pass to Gantt Chart if not complete yet
# pass to ganttChart, subprocessClass and cycle
