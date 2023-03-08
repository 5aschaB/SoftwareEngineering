import subprocessClass
import topologicalOrdering as topOrd
import costCalculations
import probabilities

#Class for storing a cycle of subprocesses
#cycleId is the ID of the cycle as stored in the database, as an integer
#baseCost is a set price of a cycle regardless of how long it takes
#predecessors is a list of other cycles' IDs that must occur before it can start, as defined in the cycle predecessor table
#subprocesses is a list of Subprocess objects that are contained as part of the cycle, as defined in the subprocess table
#repeatProbability is a dictionary with the number as the key, and the value is the probability that this cycle will repeate that number of times
#Example probabilityGraph:
#{1:0.04, 2:0.1, 3:0.125 ... 21:0.01}
#startGraph is the expected start time of the cycle, using a similar probability graph as with the subprocess object
#probabilityGraph is the expected time taken for 1 repeat of the cycle from start to finish, stored similarly to above
#finishGraph is the expected finish time of the cycle, calculated using the repeatProbability, probabilityGraph and startGraph, and uses a similar probability graph as above
#costGraph is the expected cost of a cycle, calculated using the cost per unit time and finishing graphs os each subprocess in the cycle, calculated using a similar probability graph as above

class Cycle:
	def __init__(self, cycleId, baseCost, predecessors, subprocesses, repeatProbability):
		self.cycleId=cycleId
		self.baseCost=baseCost
		self.predecessors=predecessors
		self.subprocesses=subprocesses
		self.repeatProbability=repeatProbability
		self.startGraph=dict()
		self.probabilityGraph=dict()
		self.finishGraph=dict()
		self.costGraph=dict()

	def getID(self):
		return self.cycleId

	def getBaseCost(self):
		return self.baseCost

	def getPredecessors(self):
		return self.predecessors

	def getSubprocesses(self):
		return self.subprocesses

	def setSubprocessOrder(self,subprocesses):
		self.subprocesses=subprocesses

	def getCostGraph(self):
		return self.costGraph

	def getProbabilityGraph(self):
		return self.probabilityGraph

	def getFinishingGraph(self):
		return self.finishGraph

	#Given the cycle, checks that all of its subprocesses are valid. Returns True if it is, prints an error message and returns False if not
	#Debug is a variable set for debugging the code. If debug=true, it will print an error message along with returning the False flag
	def checkSubprocesses(self,debug):
		subprocessIDs=[]
		#Checks that the list of subprocesses is actually a list
		if (isinstance(self.subprocesses,list)):
			#Checks that every element in the list is actually a Subprocess object, and that its probability graph is valid
			for i in self.subprocesses:
				if (isinstance(i,subprocessClass.Subprocess)):
					#If the probability graph of the subprocess is valid, add its ID to the list of all subprocesses in the cycle, if not, return False
					if (probability.checkProbabilityGraph(i.getProbabilityGraph(),debug)):
						subprocessIDs.append(i.getID())
					else:
						return False
					if ((isinstance(i.getMembersRequired(),int)) and (i.getMembersRequired()>0)):
						if (((isinstance(i.getCostPerTime(),float)) or (isinstance(i.getCostPerTime(),int))) and (i.getCostPerTime()>=0)) and (((isinstance(i.getBaseCost(),float)) or (isinstance(i.getBaseCost(),int))) and (i.getBaseCost()>=0)):
							pass
						#If any costs are not floating point or integer numbers, or less than 0, return false
						else:
							if debug:
								print("Error: Costs must be positive numbers\n")
							return False
					#If the number of members required is not an integer, return false
					else:
						if debug:
							print("Error: Members required is not a positive integer\n")
						return False
				#If an element in the list is not a Subprocess object, return False
				else:
					if debug:
						print("Error: Elements in list not of type Subprocess\n")
					return False
		#If the list of subprocesses is not actually a list, return False
		else:
			if debug:
				print("Error: Subprocesses should be a list\n")
			return False
		#Checks that the predecessors for every subprocess is actually a subprocess within the cycle
		for i in self.subprocesses:
			#If the predecessors is actually a list, complete the check
			if (isinstance(i.getPredecessors(),list)):
				for j in i.getPredecessors():
					#If any predecessor is not a part of the cycle, return False
					if j not in subprocessIDs:
						if debug:
							print("Error: Subprocess predecessor not part of the same cycle\nExample: "+str(i.getID())+" has predecessor "+str(j)+", but "+str(j)+" is not a subprocess in this cycle\n")
						return False
			#If the predecessors is not in list form, return False
			else:
				if debug:
					print("Error: Predecessors should be a list\n")
				return False
		#Topologically sorts the subprocesses so that a processes' predecessors occur before it, if possible
		return topOrd.topologicalOrderingSubprocesses(self,debug)

	#Works out the overall cost of a cycle based on the cost of the subprocesses within it
	def calculateCosts(self):
		#Sets the initial cost of the graph to the base cost of the cycle
		sumCost={self.baseCost:1}
		#Iterates through all of the subprocesses contained within the cycle, and adds the cost probabilities to the base cost
		for i in self.subprocesses:
			sumCost=costCalculations.addCost(sumCost,i.getBaseCost(),i.getCostPerTime(),i.getProbabilityGraph())
		#Sets the overall cost of the cycle to be the calculation of the overall cost for 1 cycle considered alongside the probability graph for n number of cycles to occur
		self.costGraph=costCalculations.cycleCosts(sumCost,self.repeatProbability)

	#Calculates the expected duration of the cycle based on the subprocesses it contains
	def calculateTimes(self):
		#Iterates through all of the subprocesses within the cycle, setting each one's start time to the one calculated
		for i in self.subprocesses:
			i.setTimeGraph(probabilities.getStartTime(i,self.subprocesses))
		#Determines which of its subprocesses are ending subprocesses (ie ones that do not have to occur before any others)
		endingSubprocesses=probabilities.getFinalProcesses(self.subprocesses)
		#Creates an arbitrary final subprocess with time 0, which relies on every other subprocess finishing, to determine the expected duration of the cycle
		finalProcess=subprocessClass.Subprocess(-1,0,0,endingSubprocesses,{0:1})
		#Calculates the expected duration of the cycle based on the expected duration of 1 cycle and the number of repeats the cycle is expected to take
		self.probabilityGraph=costCalculations.cycleCosts(probabilities.getStartTime(finalProcess,self.subprocesses),self.repeatProbability)

	#Sets the start time of the cycle to the one given, and then generates its finishing time based on its start time and expected duration
	def setTimeGraph(self,startGraph):
		self.startGraph=startGraph
		self.finishGraph=costCalculations.addCost(startGraph,0,1,self.probabilityGraph)

	#Given a list of all cycle ids that should be removed from its list of predecessors, removes them all,
	#and generates such a list for all of the subprocesses contained within it
	def removeUnnecessary(self,excessList):
		#Determines a list of pairs of subprocesses within the cycle that can be removed due to being unnecessary
		unnecessary=topOrd.unnecessaryRelation(self.subprocesses)
		for i in self.subprocesses:
			#Generates a list of all subprocess ids to be removed from the list of predecessors for that subprocess
			toRemove=[]
			for j in unnecessary:
				if j[1]==i.getID():
					toRemove.append(j[0])
			#Removes all of the unnecessary predecessors from the subprocess's list of predecessors
			i.removeUnnecessary(toRemove)
		#Removes all of the unnecessary predecessors from the cycle's list of predecessors as given as input
		for i in excessList:
			self.predecessors.remove(i)
