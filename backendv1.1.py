### backend integration

import math
import sqlalchemy
import sqlite3
import git_tracker
import riskMatrix
import AI
import ProbabilityCalculation




################### FOR EACH PROJECT ###################

## data to be retrieved: 
# projectid, alreadySpent, budget, 
# deadline, surveylist, cycles, 
# startdate, teamsize, startingteamsize



################### GANTT CHART

## create an instance of a gantt chart
thisGantt = GanttChart(projectid, cycles)


## gantt data??? todo with Josh
## what needs passing in?

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
## or independent functions - do I need to pass a Gantt object?

## create a budget metric object
budgetMetric = recordHardMetric(projectid, "budget", [alreadySpent, budget])
## create a completeness metric object
completenessMetric = recordHardMetric(projectid, "completeness")
## create a deadline metric object
deadlineMetric = recordHardMetric(projectid, "deadline", [deadline])

################### Soft metric objects

## create a team size metric object
teamSizeMetric = recordSoftMetric(projectid, "teamSize", surveylist)
## create a team morale metric object
teamMoraleMetric = recordSoftMetric(projectid, "teamMorale", surveylist)
## create a team wellness metric object
teamWellnessMetric = recordSoftMetric(projectid, "teamWellness", surveylist)

## Calculate the final project score
finalScore = final_score([budgetMetric, completenessMetric, deadlineMetric, teamSizeMetric, teamMoraleMetric, teamWellnessMetric])

## The metric objects have been created so pass these to the AI subsystem


################### PROBABILITY CALCULATION & AI ###################

## AI subsystem data feeding in??? - todo with Sam

## ProbabilityInputs()
## AIInputs ([budgetMetric, completenessMetric, deadlineMetric, teamSizeMetric, teamMoraleMetric, teamWellnessMetric])


## Probability Caluculation takes
## startdate, deadline, (subprocessdeadline?)
## budget, alreadySpent
## completenessMetric
## startteamsize, teamsize
## teamMoraleMetric
## teamWellnessMetric
## abscences maybe???

## AI takes
## array of risk matrix objects?

## no functions to call to integrate with main code as structured as 1 long file

