### backend integration

import math
import sqlalchemy
import sqlite3
import git_tracker
import riskMatrix
import AI
import ProbabilityCalculation




################### FOR EACH PROJECT ###################

## data to be retrieved from UI input/database: 
# projectid, 
# alreadySpent, 
# budget, 
# deadline,
# surveylist
# startdate (estimated starttime), 
# teamsize, 
# startingteamsize
# estimated duration



################### Soft metric objects

## create a team size metric object
teamSizeMetric = recordSoftMetric(projectid, "teamSize", surveylist)
## create a team morale metric object
teamMoraleMetric = recordSoftMetric(projectid, "teamMorale", surveylist)
## create a team wellness metric object
teamWellnessMetric = recordSoftMetric(projectid, "teamWellness", surveylist)

## create a completeness metric object
completenessMetric = recordHardMetric(projectid, "completeness")

## The metric objects have been created so pass these to the AI subsystem, returns a Gantt chart for the project
thisGantt = samFunction(teamSizeMetric, teamMoraleMetric, teamWellnessMetric, completenessMetric)
thisGantt.checkCycles(False)
thisGantt.calculateTimes()
thisGantt.calculateCosts()

################### RISK MATRIX ###################

## For each metric, create a metric object
## of the form: Metric(name, projectid, priority, score, trend, islow, timeframe)
## where name is the metric name (budget/completeness/deadline etc.)
## projectid indicates which project we are tracking
## priority is the priority score of this metric for this project (1 to 5, 5 being highest priority)
## score is the risk matrix score of the metric
## trend indicates if there was upwards (1) or downwards (-1) trend or if the scores have been consistent (0)
## islow indicates if the recemt scores of this metric have been consistently low
## timeframe is which timeframe we are tracking on the project

################### Hard metric objects

## NB - are underBudgetProbability and onTimeProbability methods
## or independent functions - do I need to pass a Gantt object? YES

## create a budget metric object
budgetMetric = recordHardMetric(projectid, "budget", [alreadySpent, budget], thisGantt)

## create a deadline metric object
deadlineMetric = recordHardMetric(projectid, "deadline", [deadline], thisGantt)

## Calculate the final project score
finalScore = final_score([budgetMetric, completenessMetric, deadlineMetric, teamSizeMetric, teamMoraleMetric, teamWellnessMetric])


################### PROBABILITY CALCULATION & AI ###################

## AI subsystem data feeding in??? - todo with Sam

AIInputs ([budgetMetric, completenessMetric, deadlineMetric, teamSizeMetric, teamMoraleMetric, teamWellnessMetric, finalScore])

## Probability Caluculation takes:
## startdate, deadline, (subprocessdeadline?= duration)
## budget, alreadySpent
## completenessMetric
## startteamsize, teamsize
## teamMoraleMetric
## teamWellnessMetric
