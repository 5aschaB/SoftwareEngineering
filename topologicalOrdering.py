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
