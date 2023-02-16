import subprocessClass
import topologicalOrdering as topOrd

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
					if (subprocessClass.checkProbabilityGraph(i.getProbabilityGraph(),debug)):
						subprocessIDs.append(i.getID())
					else:
						return False
					if ((isinstance(i.getMembersRequired(),int)) and (i.getMembersRequired()>0)):
						if (((isinstance(i.getCostPerTime(),float)) or (isinstance(i.getCostPerTime(),intt))) and (i.getCostPerTime()>=0)) and (((isinstance(i.getBaseCost(),float)) or (isinstance(i.getBaseCost(),intt))) and (i.getBaseCost()>=0)):
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
