import networkx

#Basic determiner of acyclicity. Takes in a list of pairs, with a pair (a,b) being a edge from a to b. Returns True if acyclic, otherwise returns False
def cycleCheck(edges):
    try:
        graph=networkx.DiGraph()
        graph.add_edges_from(edges)
        return networkx.is_directed_acyclic_graph(graph)
    #Returns False if input is not valid
    except:
        return False

#Takes in an input cycle, determines if it has a valid ordering and generates this if it is possible
#Debug is a variable set for debugging the code. If debug=true, it will print an error message along with returning the False flag
def topologicalOrderingSubprocesses(cycle, debug):
    #Creates a directed graph, with the subprocesses as nodes, and edges existing from subprocess i to subprocess j if subprocess i is a predecessor of j
    graph = networkx.DiGraph()
    for i in cycle.getSubprocesses():
        for j in i.getPredecessors():
            graph.add_edge(j,i.getID())
    #Determines if the graph is acyclic
    if networkx.is_directed_acyclic_graph(graph):
        #Creates a topological ordering of the graph so that no process relies on one later in the ordering to be finished before it can start
        ordering=list(networkx.topological_sort(graph))
        #Converts this ordering on the graph back in to an ordering of processes
        newSubprocessList=[]
        for i in ordering:
            for j in cycle.getSubprocesses():
                if (j.getID()==i):
                    newSubprocessList.append(j)
        #Updates the list of subprocesses in the cycle to the topological ordering for ease of future use
        cycle.setSubprocessOrder(newSubprocessList)
        return True
    #If the graph contains a cycle, there is not a valid ordering of subprocesses that allows one to be started where the others can finish, so print an error message and return false
    else:
        if debug:
            print("Error: Set of predecessors forms a cycle, so no valid schedule exists\n")
        return False

#Takes in an input ganttChart, determines if it has a valid ordering and generates this if it is possible
#Debug is a variable set for debugging the code. If debug=true, it will print an error message along with returning the False flag
def topologicalOrderingCycles(ganttChart, debug):
    #Creates a directed graph, with the cycles as nodes, and edges existing from cycle i to cycle j if cycle i is a predecessor of j
    graph = networkx.DiGraph()
    for i in ganttChart.getCycles():
        for j in i.getPredecessors():
            graph.add_edge(j,i.getID())
    #Determines if the graph is acyclic
    if networkx.is_directed_acyclic_graph(graph):
        #Creates a topological ordering of the graph so that no cycle relies on one later in the ordering to be finished before it can start
        ordering=list(networkx.topological_sort(graph))
        #Converts this ordering on the graph back in to an ordering of processes
        newCycleList=[]
        for i in ordering:
            for j in ganttChart.getCycles():
                if (j.getID()==i):
                    newCycleList.append(j)
        #Updates the list of cycles in the ganttChart to the topological ordering for ease of future use
        ganttChart.setCycleOrder(newCycleList)
        return True
    #If the graph contains a cycle, there is not a valid ordering of cycles that allows one to be started where the others can finish, so print an error message and return false
    else:
        if debug:
            print("Error: Set of predecessors forms a cycle, so no valid schedule exists\n")
        return False

#Given a list of subprocesses, returns a list of pairs of subprocess ids that are unnecessary due to transitivity
#Eg. process 1 must occur before process 2, and process 2 must occur before process 3, therefore process 1 must occur before process 3 by implication
#This is important so that a) the algorithm runs more efficiently as it will consider less predecessors each time, and
#b) the algorithm correctly identifies all parent and child subprocesses, and that this set is disjoint,
#so that the algorithm does not generate 2 separate values for the same subprocess that may conflict by assuming them to be different subprocesses
def unnecessaryRelation(subprocesses):
    #Creates a directed graph where an edge exists to every subprocess from all of its predecessors
    graph = networkx.DiGraph()
    for i in subprocesses:
        for j in i.getPredecessors():
            graph.add_edge(j,i.getID())
    unnecessary=[]
    #For every predecessor relationship, determine if it is unnecessary and if so, add it to a list
    for i in subprocesses:
        for j in i.getPredecessors():
            #Remove the edge from the directed graph in question
            graph.remove_edge(j,i.getID())
            #If there still exists a path between these 2 vertices, then the original edge must have been unnecessary
            if i.getID() in networkx.descendants(graph,j):
                unnecessary.append((j,i.getID()))
            #If no path exists after the removal of the edge, add the edge back in to the graph to maintain the implication
            else:
                graph.add_edge(j,i.getID())
    return unnecessary
