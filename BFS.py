from Algorithm import *
import time
class BFS(Algorithm):
    def __init__(self,graph, startNodeNumber, endNodeNumber, GUI = None, blocked = None):
            super().__init__(graph,startNodeNumber, endNodeNumber, GUI, blocked)
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
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        # We mark the first node as unvisited
        self.unVisited.append(currentNode)
        while(self.foundGoal != True and len(self.unVisited) != 0):
            currentNode = self.unVisited.pop(0)
            (row,col) = self.graph.getNodeIndexes(currentNode.number)
            if(self.GUI is not None):
                if(currentNode.number != self.startNodeNumber):
                    time.sleep(.05)
                    self.updatePlot(currentNode.number, "pink")
            #currentNode = self.graph.makeNodeFromNumber(currentNode.number)
            neighbors = self.graph.getNodeNeighbors(currentNode.number)
            currentNode.neighbors = neighbors
            totalPath.append(currentNode.number)
            print("Visiting: " + str(currentNode.number))
            self.visited.append(currentNode)
            for n in neighbors:
                currentNeighborNode = self.graph.makeNodeFromNumber(n)
                if(currentNeighborNode in self.visited or currentNeighborNode in self.unVisited or
                        currentNeighborNode.number in self.blocked):
                    continue
                currentNeighborNode.parent = currentNode
                print("Adding to unvisited: " + str(n) + ", Parent is: " + str(currentNeighborNode.parent.number))
                #If one of the neighbors is the node we are looking for
                if currentNeighborNode.number == self.endNodeNumber:
                    #print("Found node!")
                    self.foundGoal = True
                self.unVisited.append(currentNeighborNode)

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
            if (self.GUI is not None):
                for node in finalPath[1:-1]:
                    time.sleep(.05)
                    self.updatePlot(node, "blue")



        else:
            print("Could Not Find Node")

