# @Sam Malcolm

#~#~# PROBABILITY CALCULATION #~#~#

## IMPORT MODULES ##

from datetime import date, timedelta
from math import sqrt
import scipy.stats as st
import ganttChart
import cycle
import subprocessClass

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

def fCommits(commits, values): # takes commit tracker value and fuzzy values
    if (commits == 10):
        return(values[0]) # if metric is at 10 (highest risk value), return least positive fuzzy value
    else:
        return values[4-(commits // 2)] # otherwise, return fuzzy value equivalent to integer division of commits metric

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
        print("Metric value out of range")  # if the prior code generates invalid input, then the metric data is unsuitable
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
                                                  # coeff1 = z-value for 1st percentile divided by z-value for input percentile
                                                  # this is necessary for solving simultaneouusly for two z-values:
                                                    # z1 = (x1 - μ)/σ, z2 = (x2 - μ)/σ, where μ is the mean, and σ is the standard deviation
                                                    # we can then say that z1 * σ = (x1 - μ), and z2 * σ = (x2 - μ)
                                                    # it then follows that (z2 / z1) * (x1 - μ) = (x2 - μ)
                                                  # coeff1 is equivalent to (z2 / z1) here
                                                    # in this mean calculation, x2 = 0, since the raw value at this 1st percentile is 0 (0 weeks since beginning of subprocess)
    coeff2 = (coeff1 * deadline)                    # therefore from the prior equations, (coeff1 * x1) + (coeff1 * μ) = -μ
                                                  # coeff2 is equivalent to (coeff1 * x1) here, where x1 is the raw deadline value
    return(coeff2 / (coeff1 - 1))                 # lastly, and following on from the above reasoning, μ = coeff2 / (coeff1 - 1)

def standardDev(value, deadline, mean): # finds standard deviation of a normal distribution for a metric, takes fuzzy value, subprocess deadline and mean as inputs
    return((deadline - mean)/(round(st.norm.ppf(value), 5))) # z = (x - μ)/σ, so σ = (x - μ)/z

def rawValueToZ(rawValue, mean, sd): # finds z-value associated with a raw value (i.e. time value along the x-axis of a normal distribution), given the standard deviation and mean, to 5 d.p.
    return(round(((rawValue - mean) / sd), 5)) # z = (x - μ)/σ

def reconcileStats(metricStats, weights): # reconciles summary statistics from multiple normal distributions, takes array of metric atats and array of weightings
    m, sd = 0                                                                 # initialises variables to hold mean and standard deviation
    for i in len(metricStats):
        m += (weights[i] * (1/(sum(weights))) * metricStats[i][0])            # adds weighted mean to m
        sd += (weights[i] * ((1/(sum(weights)))**2) * (metricStats[i][1]**2)) # adds weighted variance to sd
    sd = sqrt(sd)                                                             # weighted standard deviation found from square root of variance                                                         # finds square root of sd (weighted variances), result is weighted standard deviation
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

def reconcileMetrics(startDate, projectDeadline, subprocessDuration, totalBudget, budgetUsed, commits, startingTeamSize, teamSize, morale, wellbeing, absences, priorities):
    # fuzzy logic scores associated with probability of punctual task completion
    fuzzyPercentiles = [0.35, 0.5, 0.65, 0.8, 0.95]

    # deduce suborocess deadline from start date and subprocess duration
    subprocessDeadline = startDate + timedelta(days=(subprocessDuration * 7))

    # initialise stats arrays
    deadlineStats, budgetStats, bugStats, teamSizeStats, teamMoraleStats, teamWellbeingStats, absenceStats, metricSummaryStats = []
    # the above arrays named (metric)Stats will store summary statistics pertaining to their named metric
    # metricSummaryStats will become a 2D array, storing summary statistics of all metrics desired by the user

    count = 0
    for i in priorities: # considers each element of the weightings array
        if i == 0:
            priorities.remove(i) # if a metric at position x has no weighting, then it is not required by the user, thus it is removed from the weightings array
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
                teamMoraleStats = [mean(fMoraleWellbeing(morale, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(morale, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(morale, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(teamMoraleStats)
            elif count == 5:     # weighting index 5 pertains to team wellbeing metric
                teamWellbeingStats = [mean(fMoraleWellbeing(wellbeing, fuzzyPercentiles), subprocessDeadline), standardDev(fMoraleWellbeing(wellbeing, fuzzyPercentiles), subprocessDeadline, mean(fMoraleWellbeing(wellbeing, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(teamWellbeingStats)
            elif count == 6:     # weighting index 6 pertains to absences metric
                absenceStats = [mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline), standardDev(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline, mean(fAbsences(absences, teamSize, fuzzyPercentiles), subprocessDeadline))]
                metricSummaryStats.append(absenceStats)
            else: break
        count += 1

    reconciledMean = reconcileStats(metricSummaryStats, priorities)[0]        # stores weighted mean of all desired metrics
    reconciledStandardDev = reconcileStats(metricSummaryStats, priorities)[1] # stores weighted standard deviation of all desired metrics

    return (probabilityDict(subprocessDeadline, reconciledMean, reconciledStandardDev)) # stores dictionary of cumulative probabilities as described in probabilityDict function

def cycleProbability(subprocesses, startDate, projectDeadline, subprocessDuration, totalBudget, budgetUsed, commits, startingTeamSize, teamSize, morale, wellbeing, absences, priorities):
    tenWeekProb = 1
    for i in subprocesses: # for every subprocess, generate a subprocess dictionary
        subprocessDict = reconcileMetrics(startDate, projectDeadline, subprocessDuration, totalBudget, budgetUsed, commits, startingTeamSize, teamSize, morale, wellbeing, absences, priorities)
        subprocessProb = 0
        for j in range(9): # aggregate probabilities from first 10weeks to generate a 10 week probability of completion
            subprocessProb += subprocessDict[j+1]
        tenWeekProb *= subprocessProb
    return(tenWeekProb)

# pass a list of cycles containing all relevant information, but with repeatProbability set to an empty dictionary
# the following function will populate that dictionary, thn form a gantt chart with all information in place
def ganttProbabilities(projectID, cyclesMinusRepeatProb, startDate, projectDeadline, subprocessDuration, totalBudget, budgetUsed, commits, startingTeamSize, teamSize, morale, wellbeing, absences, priorities):
    cycles = () #will contain final cycle objects with updated probabilities
    for i in cyclesMinusRepeatProb:
        subprocesses = i.getSubprocesses()
        cycleProb = cycleProbability(subprocesses)
        cycles.append(cycle(i.getID(), i.getBaseCost(), i.getPredecessors(), i.getSubprocesses(), cycleProb))

    return(ganttChart(projectID, cycles))