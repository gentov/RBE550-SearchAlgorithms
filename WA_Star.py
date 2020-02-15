from Algorithm import *
import random
import time
import sys
class WA_Star(Algorithm):
    def __init__(self, graph, startNodeNumber, endNodeNumber, GUI = None):
            super().__init__(graph,startNodeNumber, endNodeNumber, GUI)
            self.weight = 5
    def resetGraph(self):
        self.graph = Graph(nodesTall=self.graph.nodesTall, nodesWide=self.graph.nodesWide)

    # #Change get edge cost for 8 connected
    def getEdgeCost(self, parentNode, neighborNode):
        # get distance between nodes
        if ((abs(parentNode.number - neighborNode.number) == 1) or (
                abs(parentNode.number - neighborNode.number) == self.graph.nodesWide)):
            costToExplore = 1
        else:
            costToExplore = 1.41
        # print("cost:", node.number, costToExplore)
        # Backtrack to the source to see the current
        # We are going to add the cost to traverse from the parent
        # In case we have some cheaper path through a different node
        nodeCopy = parentNode
        print("Parent:", parentNode.number, "Neighbor:", neighborNode.number)
        if(nodeCopy.parent != None):
            parentNodeCost = nodeCopy.costToExplore
            # print("Parent to: ", neighborNode.number, "is: ", nodeCopy.number)
            # print("Cost of: ", nodeCopy.number, "is: ", parentNodeCost)
            costToExplore += parentNodeCost
        # return 1
        print("Total Cost to go to:", neighborNode.number, "is:", costToExplore)
        return costToExplore

    #Change get edge cost for 8 connected
    # def getEdgeCost(self, parentNode, neighborNode):
    #     # get distance between nodes
    #     seed = parentNode.number * neighborNode.number
    #     random.seed(seed)
    #     costToExplore = random.random() * 6  # 10
    #     #print("cost:", node.number, costToExplore)
    #     #Backtrack to the source to see the current
    #     #We are going to add the cost to traverse from the parent
    #     #In case we have some cheaper path through a different node
    #     nodeCopy = parentNode
    #     print("Parent:", parentNode.number, "Neighbor:", neighborNode.number)
    #     while(nodeCopy.parent != None):
    #         parentNodeCost = nodeCopy.costToExplore
    #         # print("Parent to: ", neighborNode.number, "is: ", nodeCopy.number)
    #         # print("Cost of: ", nodeCopy.number, "is: ", parentNodeCost)
    #         costToExplore += parentNodeCost
    #         #print("Node:", nodeCopy.number, "Cost:", costToExplore)
    #         nodeCopy = nodeCopy.parent
    #     #return 1
    #     print("Total Cost to go to:", neighborNode.number, "is:", costToExplore)
    #     return costToExplore

    # #Change get edge cost for 8 connected
    def getHeuristic(self, neighborNode):
        # get estimated distance to goal
        (row, col) = self.graph.getNodeIndexes(neighborNode.number)
        (rowEnd,colEnd) = self.graph.getNodeIndexes(self.endNodeNumber)
        heuristicValue = (abs(row - rowEnd)) + (abs(col - colEnd))
        print("Neighbor Node: ", neighborNode.number, "Heuristic: ", heuristicValue)
        return heuristicValue * self.weight

    def run(self):
        self.resetGraph()
        self.foundGoal = False
        del self.visited[:]
        del self.unVisited[:]
        totalPath = []
        """
         PseduoCode for Dijkstra:
         It is essentially BFS with weighted edges
         Start with the start node:
         1) For each of the neighbors, find their cost, and put them in the 
         queue according to their cost to explore (so sort neighbors before popping)
         2) This time, we can revisit nodes as long as their cost is lower!
            This is because its cost to explore could change
        """
        print("Start: ", self.startNodeNumber, "End: ", self.endNodeNumber)
        initialNode = self.startNodeNumber
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        currentNode.costToExplore = 0
        currentNode.heuristicCost =  self.getHeuristic(currentNode)
        # We mark the first node as unvisited
        self.unVisited.append(currentNode)
        #While we haven't found the goal and the length of the unvisited array > 0
        while(self.foundGoal != True and len(self.unVisited) != 0):
            #Let's explore the least expensive node
            currentNode = self.unVisited.pop(0)
            #find the nodes neighbors
            neighbors = self.graph.getNodeNeighbors(currentNode.number)
            #set the neighbors as the current node's neighbors
            currentNode.neighbors = neighbors
            if currentNode.number == self.endNodeNumber:
                # print("Found node!")
                self.foundGoal = True
            #This is for plotting: get the row and column of the node
            if (self.GUI is not None):
                if ((currentNode.number != self.startNodeNumber) and (currentNode.number != self.endNodeNumber)):
                    time.sleep(.02)
                    self.updatePlot(currentNode.number, "pink")
            #To the total path, add this node
            totalPath.append(currentNode.number)
            #Ok, we are visiting this node
            print("Visiting: " + str(currentNode.number))
            self.visited.append(currentNode.number)
            #For each of the neighbors
            for n in neighbors:
                # current neighbor node
                if(n in self.visited):
                    continue

                currentNeighborNode = self.graph.makeNodeFromNumber(n)

                # if the node does not have a parent yet
                if(currentNeighborNode.parent == None and currentNeighborNode.number != 0):
                    currentNeighborNode.parent = currentNode

                if n in self.GUI.blocked:
                    continue

                #Find the edge cost to this node
                costToExplore = self.getEdgeCost(currentNode, currentNeighborNode)
                heuristicCost = self.getHeuristic(currentNeighborNode)
                currentNeighborNode.totalCost = costToExplore + heuristicCost
                # If the new found cost is lower, we update it
                if(costToExplore < currentNeighborNode.costToExplore):
                    #if this isn't the  first time we've changed the cost of the node
                    if(currentNeighborNode.costToExplore < sys.maxsize):
                        # print("New Cost:",costToExplore, "Old Cost: ", currentNeighborNode.costToExplore)
                        print("FOUND AN ACTUAL IMPROVEMENT")
                    #update the edge cost
                    currentNeighborNode.costToExplore = costToExplore
                    currentNeighborNode.totalCost = costToExplore + self.getHeuristic(currentNeighborNode)
                    #set the new parent of the node
                    currentNeighborNode.parent = currentNode
                    print("Adding to unvisited: " + str(currentNeighborNode.number) + ", Parent is: " + str(currentNode.number), "Cost: ", currentNeighborNode.totalCost)
                    #add it back into unvisited
                    self.unVisited.append(currentNeighborNode)
            #self.visited.append(currentNode.number)
            #sort the list
            self.unVisited.sort(key=lambda x: x.totalCost)
            [print(i.number, i.totalCost) for i in self.unVisited]


        #If we have found the node
        if(self.foundGoal):
            #List to hold final path
            finalPath = []
            #Print the total path
            print("Total path taken by Dijkstra's:", totalPath)
            #We are going to look at everyone's parents
            node = currentNode
            #The last visited node is the end-node's parent, append it first
            finalPath.append(node.number)
            #While the node has a parent
            while(node.parent != None):
                #The new node under examination is the node's parent
                currentNode = currentNode.parent
                node = currentNode
                #append to the list the current node's parent's number
                finalPath.append(currentNode.number)
            # Reverse the list so that we look at children instead of parents
            finalPath.reverse()
            finalPath.append(self.endNodeNumber)
            if (self.GUI is not None):
                for node in finalPath[1:-2]:
                    time.sleep(.02)
                    self.updatePlot(node, "blue")
            print("Final path from start to end as found by Dijkstra's:" , finalPath)

        else:
            print("Could Not Find Node")
