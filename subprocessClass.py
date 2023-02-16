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
	def __init__(self, processId, membersRequired, costPerTime, baseCost, predecessors, probabilityGraph):
		self.processId=processId
		self.membersRequired=membersRequired
		self.costPerTime=costPerTime
		self.baseCost=baseCost
		self.predecessors=predecessors
		self.probabilityGraph=probabilityGraph
		self.startGraph=dict()
		self.finishGraph=dict()

	def getID(self):
		return self.processId

	def getMembersRequired(self):
		return self.membersRequired

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

#Given a probability graph, checks that this graph is valid. Returns True if valid, returns False if not valid
#Debug is a variable set for debugging the code. If debug=true, it will print an error message along with returning the False flag
def checkProbabilityGraph(probabilityGraph, debug):
	#Probability graph should be a dictionary
	if (isinstance(probabilityGraph, dict)):
		probabilityCount=0
		#Checks every key/value pair in the dictionary
		for i in probabilityGraph.keys():
			#Checks that the key is an integer.
			if (isinstance(i,int) and i>=0):
				#Checks that the value is a floating point number (could possibly be 1 if a time is guaranteed)
				if (isinstance(probabilityGraph[i],float) or (probabilityGraph[i] == 1)):
					#Checks that the value is positive (since it is a probability). If it is, add its value to the sum of probabilities. If not, return False
					if (probabilityGraph[i]<0):
						if debug:
							print("Error: Individual probability is negative.\nExample: "+str(probabilityGraph[i])+"\n")
						return False
					else:
						probabilityCount+=probabilityGraph[i]
				#If the value is not a floating point number, return False
				else:
					if debug:
						print("Error: Value type is not floating point.\nExample: "+str(probabilityGraph[i])+"\n")
					return False
			#Every key should be an integer, if not, return False
			else:
				if debug:
					print("Error: Key type is not a positive integer.\nExample: "+str(i)+"\n")
				return False
		#If the dictionary is empty, returns false
		if not probabilityGraph:
			if debug:
				print("Error: Probability graph is empty\n")
			return False
		#Checks that the sum of probabilities makes logical sense. If it is larger than 1, the probabilities do not make sense, so return False
		if (probabilityCount>1):
			if debug:
				print("Error: Probabilities sum to "+str(probabilityCount)+". This value should be less than 1\n")
			return False
		#Does a sanity check on the sum of probabilities. Typically, this should be equal to 1, but due to rounding or deliberately omitting
		#negligible probabilities for storage saving purposes, it may actually be less than 1. If it is below 0.9, it could be considered abnormally low.
		#This would not immediately prove to be an error: it may be that such rounding is valid, so it only provides a warning rather than an error
		elif ((probabilityCount<0.9)):
			if debug:
				print("Warning: Probabilities sum to "+str(probabilityCount)+". This value is valid but is not close to 1. Please check this is not an error\n")
			return True
		#If the input graph has passed all checks, return True to indicate that it is a valid probability graph
		else:
			return True
	#Probability graph should be in a dictionary, if not, return False
	else:
		if debug:
			print("Error: Input graph is not a dictionary\n")
		return False
