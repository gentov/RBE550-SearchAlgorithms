from Algorithm import *
import time
class BFS(Algorithm):
    def __init__(self,graph, startNodeNumber, endNodeNumber, window):
            super().__init__(graph,startNodeNumber, endNodeNumber, window)
    def run(self):
        self.foundGoal = False
        totalPath = []
        """
         PseduoCode for BFS:
            We mark the first node as unvisited
            then we explore the neighbors of that node, and add each one to the unvisited queue
            we have now explored the current node, so we add it to the visited queue
            We repeatedly pop the top element of the unvisited list and repeat until we reach the goal
        """
        print("Start: ", self.startNodeNumber, "End: ", self.endNodeNumber)
        initialNode = self.startNodeNumber
        #We mark the first node as unvisited
        self.unVisited.append(initialNode)
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        while(self.foundGoal != True and len(self.unVisited) != 0):
            currentNodeNumber = self.unVisited.pop(0)
            (row,col) = self.graph.getNodeIndexes(currentNodeNumber)
            if(currentNodeNumber != self.startNodeNumber):
                time.sleep(.05)
                self.updatePlot(row, col, "pink")
            currentNode = self.graph.makeNodeFromNumber(currentNodeNumber)
            neighbors = self.graph.getNodeNeighbors(currentNodeNumber)
            currentNode.neighbors = neighbors
            totalPath.append(currentNode.number)
            #print("Visiting: " + str(currentNode.number))
            self.visited.append(currentNode.number)
            for n in neighbors:
                if(n in self.visited or n in self.unVisited):
                    continue
                currentNeighborNode = self.graph.makeNodeFromNumber(n)
                currentNeighborNode.parent = currentNode
                #print("Adding to unvisited: " + str(n) + ", Parent is: " + str(currentNeighborNode.parent.number))
                #If one of the neighbors is the node we are looking for
                if n == self.endNodeNumber:
                    #print("Found node!")
                    self.foundGoal = True
                self.unVisited.append(n)

        #If we have found the node
        if(self.foundGoal):
            #List to hold final path
            finalPath = []
            #Print the total path
            print("Total path taken by BFS:", totalPath)
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
            print("Final path from start to end as found by BFS:" , finalPath)
            del self.visited[:]
            del self.unVisited [:]
            for node in finalPath[1:-1]:
                (row, col) = self.graph.getNodeIndexes(node)
                time.sleep(.05)
                self.updatePlot(row, col, "blue")



        else:
            print("Could Not Find Node")

