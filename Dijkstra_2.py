from Algorithm import *
import random
import time
import sys
class Dijkstra_2(Algorithm):
    def __init__(self, graph, startNodeNumber, endNodeNumber, GUI = None, blocked = None):
            super().__init__(graph,startNodeNumber, endNodeNumber, GUI, blocked)
    def resetGraph(self):
        self.graph = Graph(nodesTall=self.graph.nodesTall, nodesWide=self.graph.nodesWide)

    def getEdgeCost(self, parentNode, neighborNode):
        #Arbitrarty heuristic so that cost to get to node is not uniform
        #Also, we want the cost to be different depending on the parent ;)
        seed = parentNode.number*neighborNode.number
        random.seed(seed)
        costToExplore = random.random() * 6 #10
        #print("cost:", node.number, costToExplore)
        #Backtrack to the source to see the current
        #We are going to add the cost to traverse from the parent
        #In case we have some cheaper path through a different node
        nodeCopy = parentNode
        while(nodeCopy.parent != None):
            parentNodeCost = nodeCopy.parent.costToExplore
            costToExplore += parentNodeCost
            #print("Node:", nodeCopy.number, "Cost:", costToExplore)
            nodeCopy = nodeCopy.parent
        #return 1
        #print("Total Cost to go to:", node.number, "is:", costToExplore)
        return costToExplore

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
            #This is for plotting: get the row and column of the node
            (row, col) = self.graph.getNodeIndexes(currentNode.number)
            if (self.GUI is not None):
                if (currentNode.number != self.startNodeNumber):
                    time.sleep(.05)
                    self.updatePlot(currentNode.number, "pink")
            #To the total path, add this node
            totalPath.append(currentNode.number)
            #Ok, we are visiting this node
            print("Visiting: " + str(currentNode.number))
            #self.visited.append(currentNode.number)
            #For each of the neighbors
            for n in neighbors:
                #We are going to find the edge to each one of the neighbors, and add it
                #to our priority queue (nodes we haven't visited)
                #If we have visited it before
                if(n in self.unVisited):
                    #only move on if the its parent is different than our current node
                    currentNeighborNode = self.graph.makeNodeFromNumber(n)
                    if(currentNeighborNode.parent == currentNode):
                        continue
                if n in self.blocked:
                    continue
                currentNeighborNode = self.graph.makeNodeFromNumber(n)
                #Find the edge cost to this node (Change this function to include both nodes, current and neighbor)
                costToExplore = self.getEdgeCost(currentNode, currentNeighborNode)
                # If the new found cost is lower, we should replace it in the queue
                if(costToExplore < currentNeighborNode.costToExplore):
                    if(currentNeighborNode.costToExplore < sys.maxsize):
                        print("FOUND AN ACTUAL IMPROVEMENT")
                    currentNeighborNode.costToExplore = costToExplore
                    #set the new parent of the node
                    currentNeighborNode.parent = currentNode
                    print("Adding to unvisited: " + str(currentNeighborNode.number) + ", Parent is: " + str(currentNode.number), "Cost: ", costToExplore)
                    self.unVisited.append(currentNeighborNode)
                #If one of the neighbors is the node we are looking for
                if n == self.endNodeNumber:
                    #print("Found node!")
                    self.foundGoal = True
            self.visited.append(currentNode.number)
            #sort the list
            self.unVisited.sort(key=lambda x: x.costToExplore)
            [print(i.number, i.costToExplore) for i in self.unVisited]


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
                for node in finalPath[1:-1]:
                    time.sleep(.05)
                    self.updatePlot(node, "blue")
            print("Final path from start to end as found by Dijkstra's:" , finalPath)

        else:
            print("Could Not Find Node")

