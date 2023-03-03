import subprocessClass
import cycle
import topologicalOrdering as topOrd
import costCalculations
import probabilities

#Class for storing an entire Gantt chart
#projectId is the ID of the project as stored in the database, as an integer
#cycles is a list of Cycle objects that are contained as part of the project, as defined in the cyccle table
#finishGraph is a dictionary with the number as the key, and the value is the probability that the project will take this long to finish
#Example probabilityGraph:
#{1:0.04, 2:0.1, 3:0.125 ... 21:0.01}
#teamSize is the number of employees that will be working on the project
#costGraph is the expected cost of a cycle, calculated using the cost per unit time and finishing graphs os each subprocess in the cycle, calculated using a similar probability graph as above

class GanttChart:
	def __init__(self, projectId, cycles):
		self.projectId=projectId
		self.cycles=cycles
		self.teamSize=1
		self.finishGraph=dict()
		self.costGraph=dict()

	def getCycles(self):
		return self.cycles

	def setCycleOrder(self,cycles):
		self.cycles=cycles

	#Given the gantt chart, checks that all of its cycles are valid. Returns True if it is, prints an error message and returns False if not
	#Debug is a variable set for debugging the code. If debug=true, it will print an error message along with returning the False flag
	def checkCycles(self,debug):
		if ((isinstance(self.teamSize,int)) and (self.teamSize>0)):
			pass
		#If the team size is not a positive integer, return false
		else:
			if debug:
				print("Error: Team size must be a positive numbers\n")
			return False
		cycleIDs=[]
		#Checks that the list of cycles is actually a list
		if (isinstance(self.cycles,list)):
			#Checks that every element in the list is actually a Cycle object, and that its probability graph is valid
			for i in self.cycles:
				if (isinstance(i, cycle.Cycle)):
					#If the cycle is valid, add its ID to the list of all cycles in the gantt chart, if not, return False
					if (i.checkSubprocesses(debug)):
						cycleIDs.append(i.getID())
						if (((isinstance(i.getBaseCost(),float)) or (isinstance(i.getBaseCost(),int))) and (i.getBaseCost()>=0)):
							pass
						#If any base cost is not floating point or an integer number, or less than 0, return false
						else:
							if debug:
								print("Error: Costs must be positive numbers\n")
							return False
					else:
						return False
				#If an element in the list is not a Cycle object, return False
				else:
					if debug:
						print("Error: Elements in list not of type Cycle\n")
					return False
		#If the list of cycles is not actually a list, return False
		else:
			if debug:
				print("Error: Cycles should be a list\n")
			return False
		#Checks that the predecessors for every cycle is actually a cycle within the gantt
		for i in self.cycles:
			for j in i.getPredecessors():
				#If any predecessor is not a part of the cycle, return False
				if j not in cycleIDs:
					if debug:
						print("Error: Cycle predecessor not part of the same gantt Chart\nExample: "+str(i.getID())+" has predecessor "+str(j)+", but "+str(j)+" is not a cycle in this gantt chart\n")
					return False
		#Removes every unncessary predecessor for every cycle and subprocess within a cycle
		self.removeUnnecessary()
		#Topologically sorts the cycles so that a cycles' predecessors occur before it, if possible
		return topOrd.topologicalOrderingCycles(self,debug)

	#Calculates the cost of the overall project based on the sum of the costs of each cycle contained within it
	def calculateCosts(self):
		#Initialises the base cost of th project to be 0 with probability 100%
		sumCost={0:1}
		#Iterates through every cycle within the project, and adds its cost graph to the base cost
		for i in self.cycles:
			#Calculates the cost of the cycle
			i.calculateCosts()
			#Adds the cost of the cycle to the current sum of the costs
			sumCost=costCalculations.addCost(sumCost,0,1,i.getCostGraph())
		#Sets the final cost graph to be the sum of all the costs of its cycles
		self.costGraph=probabilities.normaliseProbabilities(sumCost)

	#Given how much the project has already spend and how large the project's budget is, returns the probability that the project will finish under budget
	def underBudgetProbability(self,alreadySpent,budget):
		startProbability=0
		#Sums all the probabilities of costs that are under the amount the project can still spend
		for i in self.costGraph.keys():
			if i<=(budget-alreadySpent):
				startProbability+=self.costGraph[i]
		return startProbability

	#Given how much the project has already spent, and what the budget of the project is, returns the expected cost of the project (as a median)
	def expectedCost(self,alreadySpent,budget):
		startProbability=0
		#Adds the probability of the next largest cost until the probability is greater than 50%, at which point, return the cost
		for i in sorted(self.costGraph):
			startProbability+=self.costGraph[i]
			if startProbability>=0.5:
				return i
		#Should not ever reach this line; fail-safe cost of -1 if the cost cannot be calculated, since cost can never be negative
		return -1

	#Calculates the expected finishing time of the project based on the expected durations of the cycles within it
	def calculateTimes(self):
		#For every cycle, calculate its expected duration based on its subprocesses
		for i in self.cycles:
			i.calculateTimes()
		#Iterates through all of the cycles within the gantt chart, setting each one's start time to the one calculated
		for i in self.cycles:
			i.setTimeGraph(probabilities.getStartTime(i,self.cycles))
		#Determines which of its cycles are ending cycles (ie ones that do not have to occur before any others)
		endingCycles=probabilities.getFinalProcesses(self.cycles)
		#Creates an arbitrary final cycle with time 0, and 1 repeat, which relies on every other cycle finishing, to determine the expected duration of the gantt chart
		finalProcess=subprocessClass.Subprocess(-1,0,0,[],{0:1})
		finalCycle=cycle.Cycle(-1,0,endingCycles,[finalProcess],{1:1})
		#Calculates the expected duration of the arbitrary final cycle. Necessary to do this so that the values are initialised, even though this will be 0
		finalCycle.calculateTimes()
		#Calculates the expected finish time of the project based on the expected start time of the arbitrary final cycle
		self.finishGraph=probabilities.normaliseProbabilities(probabilities.getStartTime(finalCycle,self.cycles))

	#Given the project's deadline, returns the probability that the project will finish on time
	def onTimeProbability(self,deadline):
		startProbability=0
		#Sums all the probabilities of times that are before the deadline
		for i in self.finishGraph.keys():
			if i<=deadline:
				startProbability+=self.finishGraph[i]
		return startProbability

	#Generates a list of all pairs of cycles that are unnecessary due to them already having an ancestor/descendant relationship,
	#and removes them from the list of predecessors for each cycle
	def removeUnnecessary(self):
		#Determines a list of pairs of cycles within the gantt chart that can be removed due to being unnecessary
		unnecessary=topOrd.unnecessaryRelation(self.cycles)
		for i in self.cycles:
			#Generates a list of all cycle ids to be removed from the list of predecessors for that ycle
			toRemove=[]
			for j in unnecessary:
				if j[1]==i.getID():
					toRemove.append(j[0])
			#Removes all of the unnecessary predecessors from the cycle's list of predecessors
			i.removeUnnecessary(toRemove)
