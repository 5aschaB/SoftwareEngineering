import costCalculations

#Class for storing a subprocess object
#processId is the ID of the subprocess as stored in the database, as an integer
#predecessors is a list of other subprocesses' IDs that must occur before it can start, as defined in the subprocess predecessor table
#membersRequired is the number of team members the subprocess needs to be able to complete it
#costPerTime is the amount of money it takes to run an iteration of the cycle for x amount of time
#baseCost is a set price of a cycle regardless of how long it takes
#probabilityGraph is a dictionary with the time as the key, and the value is the probability that that specific subprocess will take that abmount of time
#Example probabilityGraph:
#{1:0.04, 2:0.1, 3:0.125 ... 21:0.01}
#startGraph is the expected start time of the subprocess in relation to the start of the cycle it's within, using a similar probability graph as above
#finishGraph is the expected finish time of the subprocess, calculated using the probabilityGraph and startGraph, and uses a similar probability graph as above

class Subprocess:
	def __init__(self, processId, costPerTime, baseCost, predecessors, probabilityGraph):
		self.processId=processId
		self.costPerTime=costPerTime
		self.baseCost=baseCost
		self.predecessors=predecessors
		self.probabilityGraph=probabilityGraph
		self.startGraph=dict()
		self.finishGraph=dict()

	def getID(self):
		return self.processId

	def getMembersRequired(self):
		return 1

	def getCostPerTime(self):
		return self.costPerTime

	def getBaseCost(self):
		return self.baseCost

	def getPredecessors(self):
		return self.predecessors

	def getProbabilityGraph(self):
		return self.probabilityGraph

	def getFinishingGraph(self):
		return self.finishGraph

	#Sets the start time of the process to the one given, and then generates its finishing time based on its start time and expected duration
	def setTimeGraph(self,startGraph):
		self.startGraph=startGraph
		self.finishGraph=costCalculations.addCost(startGraph,0,1,self.probabilityGraph)

	#Given a list of all subprocess ids that should be removed from its list of predecessors, removes them all
	def removeUnnecessary(self,excessList):
		for i in excessList:
			self.predecessors.remove(i)
