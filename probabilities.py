import subprocessClass
import networkx

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

#Due to rounding, a probability graph may not sum to 1 (or even near 1). This function proportionally adjusts the probabilities in a probability graph so that the sum of the probabilities is 1
def normaliseProbabilities(probabilityGraph):
	#Calculates the sum of all probabilities in the probability graph
	totalProbabilities=0
	for i in probabilityGraph.keys():
		totalProbabilities+=probabilityGraph[i]
	#Adjust the probabilities in the probability graph so that the total sum will be 1
	for i in probabilityGraph.keys():
		probabilityGraph[i]=round((probabilityGraph[i]/totalProbabilities),6)
	#Removes any 0 probability elements after normalisation
	if probabilityGraph[i]==0:
		del probabilityGraph[i]
	return probabilityGraph

#Given 2 probability graphs, calculates the probability of each one finishing later than the other
def addFinishingTimes(subprocessGraph1,subprocessGraph2):
	finish=dict()
	for i in subprocessGraph1.keys():
		for j in subprocessGraph2.keys():
			#Calculates the probability of 2 subprocesses finishing at certain times
			prob=subprocessGraph1[i]*subprocessGraph2[j]
			#The finishing time is the subprocess that finishes last
			if i>j:
				finishTime=i
			else:
				finishTime=j
			#If the finshing time calculated has already been added to the dictionary, add the probability to it
			if finishTime in finish.keys():
				finish[finishTime]+=prob
			#If the sum finishing time does not already have a probability stored, add it to the dictionary
			else:
				finish.update({finishTime:prob})
	#Rounds all of the probabilities to 6 decimal places and then removes any that have been rounded to 0
	for i in finish.keys():
		finish[i]=round(finish[i],6)
		if finish[i]==0:
			del finish[i]
	#Return the final probability finishing times
	return finish

#Given a list of predecessors, returns a list of subprocesses that are not independent of each other
def getConnectedSubprocess(predecessors):
	graph=networkx.Graph()
	#Stores a list of the IDs of all the subprocesses of the main subprocess
	children=[]
	for i in predecessors:
		children.append(i.getID())
		#Adds an edge between every subprocess and its predecessor
		for j in i.getPredecessors():
			graph.add_edge(i.getID(),j)
	components=[]
	#Generates the connected components as an iterator over sets
	for i in networkx.connected_components(graph):
		#Generates each connected component as a list, only accepting IDs of the parents (by checking them against the original list)
		connectedComponent=[]
		for j in i:
			if j in children:
				connectedComponent.append(j)
				#Removes the ID from the original list of all IDs, so that the left over list will all be subprocesses not included in the graph (due to them not having any predecessors)
				children.remove(j)
		#Adds the specific comnnected component to the list of all connected components
		components.append(connectedComponent)
	#Iterates over the remaining subprocess IDs and adds them as singletons to the list of connected components
	for i in children:
		components.append([i])
	#Returns the list of connected components
	return components

#Given a dictionary and an index, returns the key at the index in the dictionary
def getKeyNumber(dictionary,index):
	counter=0
	for i in dictionary.keys():
		if counter==index:
			return i
		else:
			counter+=1
	return False

#Given a list of subprocesses and an id, returns the subprocess with the given id
def getSubprocess(list,id):
	for i in list:
		if i.getID()==id:
			return i
	return False

#Given a dependent list of subprocesses and their predecessors, generates a finishing graph
def generateComponentProbability(parentSubprocesses,childSubprocesses):
	#If the number of total parent subprocesses is 1, then its finishing time is the only valid finishing time for the set of subprocesses,
	#which will therefore reduce the amount of computation needed by running this shortcut
	if len(parentSubprocesses)==1:
		return parentSubprocesses[0].getFinishingGraph()
	#Runs the more complex algorithm in the case that there are more than one parent subprocesseses
	else:
		probabilities=dict()
		ids=[]
		selection=[]
		selectionCount=[]
		for i in parentSubprocesses:
			#For every parent subprocess, adds to the dictionary the key of the subprocess and the value is a pair,
			#the first being the probability graph of the subprocess and the second being the index of its assigned values in the other arrays
			probabilities.update({i:(i.getProbabilityGraph(),len(ids))})
			#Stores all subprocesses in 1 array for ease of iteration
			ids.append(i)
			#Stores the current assignment and its index in 2 separate arrays for that subprocess (initially the first value in the probability graph)
			selection.append(getKeyNumber(probabilities[i][0],0))
			selectionCount.append(0)
		#As above, but for the child subprocesses, and the graph stored is its finishing time probability graph rather than the one for its duration
		for i in childSubprocesses:
			probabilities.update({i:(i.getFinishingGraph(),len(ids))})
			ids.append(i)
			selection.append(getKeyNumber(probabilities[i][0],0))
			selectionCount.append(0)
		totalTimes=dict()
		withinList=True
		#Iterates through every possible combination of child subprocess finishing times and parent subprocess durations,
		#calculating the overall finishing time for each possibility and its associeated probability, before storing it in the graph
		while withinList:
			end=0
			#Iterates through every parent subprocess, calculating its start time using the predecessors' finishing times,
			#and using its duration to calculate and end time, and then stores the maximum of these values to find the subprocess with the latest end time
			for i in parentSubprocesses:
				start=0
				#Iterates through each of the predecessors of the parent subprocesses, updating the start time to be the maximum finishing time of its predecessors
				for j in i.getPredecessors():
					#If the finishing time of the predecessor is greater than that of all the others previously calculated, update the new start time accordingly
					if selection[probabilities[getSubprocess(childSubprocesses,j)][1]]>start:
						start=selection[probabilities[getSubprocess(childSubprocesses,j)][1]]
				#If the calculated end time of the subprocess is later than the currently stored one, update it accordingly
				if (start+selection[probabilities[getSubprocess(parentSubprocesses,i.getID())][1]])>end:
					end=start+selection[probabilities[getSubprocess(parentSubprocesses,i.getID())][1]]
			#Calculates the probability of the specific scenario occurring by multiplying the individual probabilities together
			probability=1
			for i in range(len(ids)):
				probability*=probabilities[ids[i]][0][selection[i]]
			#Adds the probability calculated to the value stored for that particular end time in the dicitonary
			if end in totalTimes.keys():
				totalTimes[end]+=probability
			else:
				totalTimes.update({end:probability})
			idPointer=0
			#Generates the next combination of possibilities, if there are none then break the loop
			while True:
				#If the array pointer reaches a number larger than that of the array, there must be no new possible combination, so break the loops
				if idPointer>=len(selection):
					withinList=False
					break
				#Select the next value for the variable currently selected
				selectionCount[idPointer]+=1
				#If the next selection is out of range of the possiblities for that variable, set it back to the start variable and run the loop again
				#to increment the next variable instead
				if selectionCount[idPointer]>=len(probabilities[ids[idPointer]][0].keys()):
					selectionCount[idPointer]=0
					idPointer+=1
				#If the selection is not out of range, the selection must be a new valid assignment, so break the inner loop
				else:
					break
			#Update the values for each variable so that they are not simply indexes of the dicitonary
			for i in range(len(selection)):
				selection[i]=getKeyNumber(probabilities[ids[i]][0],selectionCount[i])
		#Return the dicitonary of the probability for all possible finishing times
		return totalTimes

#Given a subprocess to generate the start time of, and a list of all subprocesses, generates the expected start time of the given subprocess
def getStartTime(subprocess,allSubprocesses):
	#Generates a list of all subprocesses whose ids are in that of the predecessor of the given subprocess
	predecessors=[]
	for i in allSubprocesses:
		if i.getID() in subprocess.getPredecessors():
			predecessors.append(i)
	#Generates a list of lists of predecessors of the next subprocess whose probabilities are dependent of each other, so must be calculated at the same time
	independentProcesses=getConnectedSubprocess(predecessors)
	allProbabilities=[]
	#Generates the finishing probability of each independent component
	for i in independentProcesses:
		#Generates a list of all subprocesses whose ids are within the connected component being considered
		parentSubprocesses=[]
		for j in allSubprocesses:
			if j.getID() in i:
				parentSubprocesses.append(j)
		#Generates a list of ids of all subprocesses whose ids are within the predecessors of any of the parent subprocesses
		childIDs=[]
		for j in parentSubprocesses:
			for k in j.getPredecessors():
				if k not in childIDs:
					childIDs.append(k)
		#Generates a list of all subprocesses whose ids are within the list of child ids
		childSubprocesses=[]
		for j in allSubprocesses:
			if j.getID() in childIDs:
				childSubprocesses.append(j)
		#Adds the finishing graph for the list of subprocesses to the list
		allProbabilities.append(generateComponentProbability(parentSubprocesses,childSubprocesses))
	#Calculates the probability of all subprocesses finishing be a certain time (ie the start time of the next subprocess), by merging each probability graph 1 by 1
	startFinalProbability={0:1}
	for i in allProbabilities:
		startFinalProbability=addFinishingTimes(startFinalProbability,i)
	#Returns the final finishing time probabilities
	return startFinalProbability

#Given a list of subprocesses, calculates the generates a list of all subprocesses that must finish to indicate the whole cycle has finished
def getFinalProcesses(subprocesses):
	nonFinal=[]
	#Creates a list of all IDs of subprocesses that are a predecessor to some other subprocess
	for i in subprocesses:
		for j in i.getPredecessors():
			if j not in nonFinal:
				nonFinal.append(j)
	final=[]
	#Creates a list of all IDs of subprocesses that are not listed as a predecessor, and are therefore counted as final subprocesses
	for i in subprocesses:
		if i.getID() not in nonFinal:
			final.append(i.getID())
	return final
