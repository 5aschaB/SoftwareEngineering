#__author__ = "Sascha Bharath"
#__version__ = "2.2"
#__project__ = "CS261 Group Project"
#__status__ = "Integration"

import math
import git_tracker
import requests
import json
import sqlalchemy
import sqlite3
import risk_matrix
import ganttChart
import backend
from Flask-React import *
import AI


################### METRIC CLASS ###################

class Metric:
  def __init__(self, name, projectid, priority, score, trend, islow, timeframe):
    self.name = name
    self.projectid = projectid
    self.priority = priority
    self.score = score
    self.trend = trend
    self.islow = islow
    self.timeframe = timeframe

################### MAIN CODE ###################


######################
## recordSoftMetric: Function that calculates the risk matrix score and returns an object for a specified soft metric
## parameters: projectid (int), metric (string), scorelist (list)
## return: s_metric (Metric object)
######################
def recordSoftMetric(projectid, metric, scorelist):
    ## get the timeframe for this metric recording
    timeframe = getLastTimeframe(projectid)
    ## calculate the average of the survey scores (then multiply by 2 because they are out of 5)
    new_score = (sum(scorelist)/len(scorelist))*2
    ## number of timeframes which are the most recent 20% of all timeframes
    n = math.ceil(numberOfTimeframes * 0.2)

    ## check if the score of this metric has been decreasing over recent timeframes
    score_trend= scoreTrend(projectid, metric, n)
    ## check if the score has been low (<=2) over recent timeframes
    score_low = scoreLow(projectid, metric, n)

    ## if the score was decreasing or low, subtract a bias constant from the score
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
    s_metric = Metric(metric, projectid, priority, newscore, score_trend, score_low, timeframe)
    return s_metric

######################
## recordSoftMetric: Function that calculates the score and creates an object for a hard metric
## parameters: projectid (int), metric (string), paramlist (list), thisGantt (Gantt object)
## return: h_metric (Metric object)
######################
def recordHardMetric(projectid, metric, paramlist, thisGantt):
    ## timeframe for this metric recording
    timeframe = getLastTimeframe(projectid)

    ## determine which hard metric we are recording
    if metric=="budget":
        ## retrieve probability of staying on budget from the Gantt Subsystem
        ## paramlist has been passed the alreadySpent and budget
        budget_probability = thisGantt.underBudgetProbability(paramlist[0], paramlist[1])
        budget_progress = 10 * budget_probability
        newscore = budget_progress
    elif metric=="completeness":
        ## assess number of commits to repo
        newscore =  git_progress(projectid, timeframe)
    elif metric=="deadline":
        ## retrieve probability of staying on budget from the Gantt Subsystem
        ## paramlist has been been passed the deadline and budget
        time_probability = thisGantt.onTimeProbability(paramlist[0])
        time_progress = 10* time_probability
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
    h_metric = Metric(metric, projectid, priority, newscore, score_trend, score_low, timeframe)
    return h_metric

######################
## isPriority: Function returns a boolean as to whether the metric is a priority for that project
## parameters: projectid (int), metric (string)
## return: (boolean)
######################
def isPriority(projectid, metric):
    pass
    ## perform SQL query on database to fetch the metric's priority
    query = "SELECT priority FROM projectMetricsTable WHERE projectid= :projectid AND metric= :metric;"
    result = db.execute(query, projectid=projectid).fetchall()
    if priority >=3:
        return True
    else:
        return False

######################
## scoreTrend: Function returns an integer as to whether the metric score has had an upwards or downwards trend or has stayed the same for the last n timeframes of the project
## parameters: projectid (int), metric (string), n (int)
## return: (int) 1 indicating an upwards trend, 0 indicating constant and -1 indicating downwards trend
######################
def scoreTrend(projectid, metric, n):
    query = "SELECT score FROM projectMetricsTable WHERE projectMetricsTable.projectid= :projectid AND projectMetricsTable.metric= :metric ORDER BY timeframe LIMIT :n;"
    #result = db.execute(query,  projectid=projectid, metric=metric, n=n).fetchall()
    scorelist = []
    increasing_scores = scorelist.sort()
    decreasing_scores = scorelist.sort(reverse=True)
    trend = 0
    
    ## check if the scores are strictly increasing (linearly)
    trend = 1
    for i in range(0, len(scorelist)):
        if scorelist[i]!=increasing_scores[i]:
            trend = 0
    ## check if the scores are strictly decreasing (linearly)
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

######################
## scoreLow: Function returns a boolean as to whether the score was low for the last n timeframes of the project
## parameters: projectid (int), metric (string), n (int)
## return: low (boolean)
######################
def scoreLow(projectid, metric, n):
    query = "SELECT score,timeframe FROM projectMetricsTable WHERE projectid= :projectid AND metric= :metric ORDER BY timeframe LIMIT :n;"
    # result = db.execute(query,  projectid=projectid, metric=metric, n=n).fetchall()
    timeframes = []
    low = True
    for i in timeframes:
        if i[1] > 2:
            low = False
    return low

######################
## numberOfTimeframes: Function returns the total number of timeframes that have been recorded for this project so far
## parameters: projectid (int)
## return: count (int)
######################
def numberOfTimeframes(projectid):
    count = 0
    query = "SELECT COUNT(timeframe) FROM projectMetricsTable WHERE projectMetricsTable.projectid= :projectid;"
    #result = db.execute(query, projectid=projectid).fetchall()
    return count

######################
## scoreLow: Function returns the number of the last recorded timeframe for this project
## parameters: projectid (int)
## return: timeframe (int)
######################
def getLastTimeframe(projectid):
    timeframe = 0
    query = "SELECT timeframe FROM projectMetricsTable WHERE projectMetricsTable.projectid= :projectid ORDER BY timeframe DESC LIMIT 1;"
    #result = db.execute(query, projectid=projectid).fetchall()
    return timeframe

######################
## final_score: Function calculates the final risk score of the project combining all the metrics and returns a score
## parameters: metric_list (list of Metric objects)
## return: score (int)
######################
def final_score(metrics_list):
    metric_sum = 0
    for m in metrics_list:
        metric_sum += m.score
    ## returns score of 1 to 5
    score = math.round(((metric_sum/len(metrics_list))/2))
    return score

