#__author__ = "Sascha Bharath"
#__version__ = "1.6"
#__project__ = "CS261 Group Project"
#__status__ = "Production"

import math
import sqlalchemy
import git_tracker

################### METRIC CLASSES ###################

## Parent class of all metrics
class Metric:
  def __init__(self, name, projectid, priority, score, trend, islow, timeframe):
    self.name = name
    self.projectid = projectid
    self.priority = priority
    self.score = score
    self.trend = trend
    self.islow = islow
    self.timeframe = timeframe

class SoftMetric(Metric):
  def __init__():
      pass
      ## flags for wellbeing risk?
    
class HardMetric(Metric):
  def __init__():
      pass
      ## flags for time/budget risk?

################### METRIC FUNCTIONS ###################

## function that calculates the score and creates an object for a soft metric
def recordSoftMetric(projectid, metric, scorelist):
    ## timeframe for this metric recording
    timeframe = getLastTimeframe(projectid) + 1
    ## calculate the average of the survey scores
    new_score = sum(scorelist)/len(scorelist)
    ## the most recent timeframes, the last 20% of those recorded
    n = math.ceil(numberOfTimeframes * 0.2)

    ## check if the score has been decreasing over recent timeframes
    score_trend= scoreTrend(projectid, metric, n)
    ## check if the score has been low (<=2) over recent timeframes
    score_low = scoreLow(projectid, metric, n)

    ## if the score was decreasing or low, subtract bias constant from the score
    if ((score_trend<0) or score_low):
        new_score -= 1

    ## if the metric is a priority, multiply by bias constant
    priority = isPriority(projectid, metric)
    if priority:
        newscore *=0.9
        priority = True

    ## round the score to the nearest integer from 1 to 10
    newscore = round(newscore)
    if newscore<1:
        newscore = 1
    if newscore>10:
        newscore = 10
        
    ## create a soft metric object then return it
    s_metric = SoftMetric(metric, projectid, priority, newscore, score_trend, score_low, timeframe)

## function that calculates the score and creates an object for a soft metric
def recordHardMetric(projectid, metric, username, repository):
    ## timeframe for this metric recording
    timeframe = getLastTimeframe(projectid) + 1

    if metric=="budget":
        ## Josh's gantt_budget %
        gantt_budget = 100
        budget_progress = 0.1* gantt_budget
        newscore = budget_progress
    elif metric=="completeness":
        ## assess number of commits to repo
        newscore =  git_progress(projectid, timeframe, username, repository)
    elif metric=="deadline":
        ## Josh's gantt_time %
        gantt_time = 100
        time_progress = 0.1* gantt_time
        newscore = time_progress
    else:
        pass

    if metric!="completeness":
        ## the most recent timeframes, the last 20% of those recorded
        n = math.ceil(numberOfTimeframes * 0.2)

        ## if the budget has been decreasing or has been low for the last n timeframes, subtract a bias constant
        ## check if the score has been decreasing over recent timeframes
        score_trend= scoreTrend(projectid, metric, n)
        ## check if the score has been low (<=2) over recent timeframes
        score_low = scoreLow(projectid, metric, n)

        ## if the score was decreasing or low, subtract bias constant from the score
        if ((score_trend<0) or score_low):
            newscore -= 1

    ## if the metric is a priority, multiply by bias constant
    if isPriority(projectid, metric):
        newscore *=0.9
        priority = True

    ## round the score to the nearest integer from 1 to 10
    newscore = round(newscore)
    if newscore<1:
        newscore = 1
    if newscore>10:
        newscore = 10

    ## create a hard metric object then return it
    h_metric = HardMetric(metric, projectid, priority, newscore, score_trend, score_low, timeframe)

## returns a boolean as to whether the metric is a priority for that project
def isPriority(projectid, metric):
    pass
    ## perform SQL query on database to determine if the metric is a priority
    ## discuss with Rishi, there is no way to currently record priority, but should be something like:
    # "SELECT metric,priority FROM projectMetricsTable/projectPriorityTable WHERE ...Table.projectid=projectid;"

## returns an integer as to whether the metric score has had an upwards or downwards trend
## or has stayed the same for the last n timeframes of the project
def scoreTrend(projectid, metric, n):
    #"SELECT ?,metric FROM projectMetricsTable WHERE projectMetricsTable.projectid=projectid ORDER BY ? LIMIT n;"
    scorelist = []
    increasing_scores = scorelist.sort()
    decreasing_scores = scorelist.sort(reverse=True)
    trend = 0
    
    ## check if the scores are increasing linearly
    trend = 1
    for i in range(0, len(scorelist)):
        if scorelist[i]!=increasing_scores[i]:
            trend = 0
    ## check if the scores are decreasing linearly
    trend = -1
    for j in range(0, len(scorelist)):
        if scorelist[j]!=decreasing_scores[j]:
            trend = 0
    
    ## if they are not increasing or decreasing linearly, then they changed inconsistently or the trend didn't change
    ## check if they did increase overall to the highest recording by comparing the last score to the highest
    if scorelist[-1]==increasing_scores[-1]:
        trend = 1
    ## check if they did decrease overall to the lowest recording by comparing the last score to the lowest
    elif scorelist[-1]==decreasing_scores[-1]:
        trend = -1
    else:
    ## neither an upwards nor downwards trend was detected so they have stayed the same
        trend = 0

    return trend
    
## returns a boolean as to whether the score was low for the last n timeframes of the project
def scoreLow(projectid, metric, n):
    # "SELECT ?,metric FROM projectMetricsTable WHERE projectMetricsTable.projectid=projectid ORDER BY ? LIMIT n;"
    timeframes = []
    low = True
    for i in timeframes:
        if i[1] > 2:
            low = False

    return low

## returns the total number of timeframes that have been recorded for this project so far
def numberOfTimeframes(projectid):
    count = 0
    # "SELECT COUNT(*) FROM projectMetricsTable WHERE projectMetricsTable.projectid=projectid;"
    return count

## returns the number of the last recorded timeframe for this project
def getLastTimeframe(projectid):
    timeframe = 0
    # "SELECT timeframe FROM projectMetricsTable WHERE projectMetricsTable.projectid=projectid ORDER BY timeframe DESC LIMIT 1;"
    return timeframe

