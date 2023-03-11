#Function used to calculate a total cost of a graph, given a cost graph and a subprocess' probability graph
#Cost graph is the initial cost graph that the new subprocess graph is being added to
#baseCost is the constant cost of a subprocess to complete
#costPerTime is a multiplier for the probability graph, representing a cost factor applied to the overall timeframe that a subprocess will take
#subprocessGraph is the duration probability graph of the subprocess. used to add to the total cost
def addCost(costGraph, baseCost, costPerTime, subprocessGraph):
    finalCost=dict()
    for i in costGraph.keys():
        for j in subprocessGraph.keys():
            #Calculates the probability of 2 costs happening at the same time
            prob=costGraph[i]*subprocessGraph[j]
            #If the sum of the 2 costs calculated already has a probability stored, add the new probability to it
            if (i+j+baseCost) in finalCost.keys():
                finalCost[i+costPerTime*j+baseCost]+=prob
            #If the sum of the costs does not already have a probability stored, add it to the dictionary
            else:
                finalCost.update({(i+costPerTime*j+baseCost):prob})
    #Rounds all of the probabilities to 6 decimal places and then removes any that have been rounded to 0
    for i in finalCost.keys():
        finalCost[i]=round(finalCost[i],6)
        if finalCost[i]==0:
            del finalCost[i]
    #Return the final probability cost graph
    return finalCost

#Calculates the cost graph of a cycle given the cost graph for its 1 cycle and the probability graph for multiple cycles
def cycleCosts(costGraph,cycleGraph):
    #Initialises a start graph with no cycles to have cost 0 with 100% probability as a base case
    currentIteration=0
    currentCostGraph={0:1}
    repeatCosts=dict()
    #Iterate through every possible number of cycles, starting with the lowest number first
    for i in sorted(cycleGraph):
        #In the case when we haven't yet produced a probability graph for the smallest number of cycles, takes a shortcut to efficiently produce this first graph
        if (currentIteration==0):
            #Creates a list of rules to follow for this shortcut method
            currentCycles=i
            cyclesList=[]
            while currentCycles>=1:
                #In the case when the number of cycles to produce is even, we need to double the graph produced by this number/2
                #This will prevent the need to simply add 1 every time and instead can double the cycles required, therefore taking log(n) steps instead of n steps
                if (currentCycles%2)==0:
                    cyclesList.append(0)
                    currentCycles=currentCycles/2
                #In the case that the number of cycles to produce is odd, we need to add the cost of 1 cycle to the graph produced by this number -1,
                #so that this number can then be halved on the next iteration
                else:
                    cyclesList.append(1)
                    currentCycles-=1
            #Iterates through the list of rules, applying each rule as necessary
            for j in range(len(cyclesList)):
                #If the rule states that the step is a doubling step, merge the current cost graph with itself to double the cycles produced
                if cyclesList[-j-1]==0:
                    currentCostGraph=addCost(currentCostGraph,0,1,currentCostGraph)
                    currentIteration*=2
                #If the rule states that the step is a +1 step, merge the current cost graph with the cost graph for 1 cycle to increase the cycles produced by 1
                else:
                    currentCostGraph=addCost(currentCostGraph,0,1,costGraph)
                    currentIteration+=1
            #Once this iteration has finished, it will be storing a graph valid for the smallest possible number of cycles
        #For a general case, we should merge the current cost graph with the cost graph for 1 cycle until we reach a point where the new cost graph represents the next number of cycles
        #It is expected that the next number of cycles would be close to the previous one, if not consecutive, and therefore this will not take much time
        while (i>currentIteration):
            currentCostGraph=addCost(currentCostGraph,0,1,costGraph)
            currentIteration+=1
        #Store the probability graph for each possible number of cycles in a new dictionary
        repeatCosts.update({i:dict(currentCostGraph)})
    output=dict()
    #Iterates through every number of cycles, multiplying the probability that number of cycles will occur by its probability graph to get the overall probability
    for i in cycleGraph.keys():
        for j in repeatCosts[i]:
            if j in output.keys():
                output[j]+=cycleGraph[i]*repeatCosts[i][j]
            else:
                output.update({j:cycleGraph[i]*repeatCosts[i][j]})
    #Rounds all of the probabilities to 6 decimal places and then removes any that have been rounded to 0
    for i in output.keys():
        output[i]=round(output[i],6)
        if output[i]==0:
            del output[i]
    #Return the final probability cost graph for the cycle
    return output
