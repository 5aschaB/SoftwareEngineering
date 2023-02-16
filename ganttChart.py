import subprocessClass
import cycle
import topologicalOrdering as topOrd

#Class for storing an entire Gantt chart
#projectId is the ID of the project as stored in the database, as an integer
#cycles is a list of Cycle objects that are contained as part of the project, as defined in the cyccle table
#finishGraph is a dictionary with the number as the key, and the value is the probability that the project will take this long to finish
#Example probabilityGraph:
#{1:0.04, 2:0.1, 3:0.125 ... 21:0.01}
#teamSize is the number of employees that will be working on the project
#costGraph is the expected cost of a cycle, calculated using the cost per unit time and finishing graphs os each subprocess in the cycle, calculated using a similar probability graph as above

class GanttChart:
	def __init__(self, projectId, cycles, teamSize):
		self.projectId=projectId
		self.cycles=cycles
		self.teamSize=teamSize
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
		#Topologically sorts the cycles so that a cycles' predecessors occur before it, if possible
		return topOrd.topologicalOrderingCycles(self,debug)
