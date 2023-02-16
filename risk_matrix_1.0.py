#__author__ = "Sascha Bharath"
#__version__ = "1.0"
#__project__ = "CS261 Group Project"
#__status__ = "Production"

################### METRIC CLASSES ###################

## Parent class of all metrics
class Metric:
  def __init__(self, name, score, projectid):
    self.name = name
    self.projectid = projectid
    self.priority = priority


class SoftMetric(Metric):
  def __init__():
      pass

    
class HardMetric(Metric):
  def __init__():
      pass


################### METRIC FUNCTIONS ###################

## function that calculates the score and creates an object for a soft metric
def record_soft_metric(projectid, metric, scorelist):
    ## calculate the average of the survey scores
    new_score = sum(scorelist)/len(scorelist)
    # n = ceil(number of all the timeframes * 0.2)

    ## check if the score has been decreasing over recent timeframes
    score_decrease = scoreTrend(projectid, metric, n)
    ## check if the score has been low (<=2) over recent timeframes
    score_low = scoreLow(projectid, metric, n)

    ## if the score was decreasing or low, subtract bias constant from the score
    if ((score_decrease<0) or score_low):
        new_score -= 0.5

    ## if the metric is a priority, multiply by bias constant
    if isPriority(projectid, metric):
        newscore *=0.9

    ## round the score to the nearest integer from 1 to 5
    newscore = round(newscore)
    if newscore<1:
        newscore = 1
    if newscore>5:
        newscore = 5
        
    ## create a soft metric object
    s_metric = SoftMetric(metric, newscore, projectid, priority)
    
    ## return the object
    return s_metric



## returns a boolean as to whether the metric is a priority for that project
def isPriority((projectid, metric)):
    pass

## returns an integer as to whether the metric score has had an upwards or downwards tren
## or has stayed the same for the last n timeframes of the project
def scoreTrend(projectid, metric, n):
    pass

## returns a booleab as to whether the score was low for the last n timeframes of the project
def scoreLow(projectid, metric, n):
    pass
