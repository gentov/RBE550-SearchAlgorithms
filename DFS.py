from Algorithm import *
import time
class DFS(Algorithm):
    def __init__(self, graph, startNodeNumber, endNodeNumber, GUI = None):
            super().__init__(graph, startNodeNumber, endNodeNumber, GUI)
    def run(self):
        #NOTE: THE UNVISITED ARRAY WILL HOLD THE NEXT TO VIEW
        self.foundGoal = False
        totalPath = []
        stack = []
        """
         PseduoCode for DFS:
         Expand a node
         Choose a neighbor (if applicable)
         No new neighbors? Backtrack one node and go to unvisited neighbors
         Repeat till goal reached
         Source:
         https://www.youtube.com/watch?v=iaBEKo5sM7w
        """
        print("Start: ", self.startNodeNumber, "End: ", self.endNodeNumber)
        initialNode = self.startNodeNumber
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        #stack.append(currentNode.number)
        #We mark the first node as unvisited
        self.unVisited.append(currentNode)
        while(self.foundGoal != True and len(self.unVisited) != 0):
            time.sleep(float(1)/self.GUI.speed.get())
            #pop the unvisited node off the top
            # currentNodeNumber = stack.pop(0)
            currentNode = self.unVisited.pop(0)
            if (self.GUI is not None):
                if (currentNode.number != self.startNodeNumber):
                    self.updatePlot(currentNode.number, "pink")
            print("Visiting: ", currentNode.number)
            if (self.GUI.fourConnected.get()):
                neighbors = self.graph.getFourNodeNeighbors(currentNode.number)
            else:
                neighbors = self.graph.getNodeNeighbors(currentNode.number)
            print("Node Neighbors are: ", neighbors)
            currentNode.neighbors = neighbors
            #this node has no neighbors, so our current node becomes the current node's parent
            if len(neighbors) == 0:
             #   print(currentNodeNumber, " has no neighbors.")
                currentNode = currentNode.parent
                continue
            #append the current node to the total path
            totalPath.append(currentNode.number)
            #add the current node to the visited list
            self.visited.append(currentNode)
            #Append to the unvisited array (our stack), the first neighbor we explore, and then break
            # if(self.endNodeNumber in neighbors):
            #     self.foundGoal = True
            canGoDeeper = False
            for i in range(len(neighbors)):
                #We only want to check a neighbot if it is not blocked, otherwise, we don't do anything
                #I can't just do: if in blocked continue, because if the last node is blocked, we won't ever backtrack
                if (neighbors[i] in self.GUI.blocked):
                    continue
                #if the current neighbor has not been visited
                if(self.graph.makeNodeFromNumber(neighbors[i]) not in self.visited):
                    currentNeighborNode = self.graph.makeNodeFromNumber(neighbors[i])
                    currentNeighborNode.parent = currentNode
                    self.unVisited.append(currentNeighborNode)
                    nextNodeToVisit = currentNeighborNode
                    if(nextNodeToVisit.number == self.endNodeNumber):
                        self.foundGoal = True
                    canGoDeeper = True
                    break
            # If you have iterated through all the neighbor nodes and we can't go deeper, backtrack one:
            if (not canGoDeeper):
                nextNodeToVisit = currentNode.parent
                self.unVisited.append(nextNodeToVisit)
                print("Backtracking")


            # #check if we have returned to the start OR we have been stuck on the same node
            # if(nextNodeToVisit.number == initialNode): # or nextNodeToVisit == currentNode.number):
            #   #  print("Next node to visit is: ", nextNodeToVisit, ". Returned to the start.")
            #     break
            #print("Next node to visit: ", nextNodeToVisit)

        #If we have found the node
        if(self.foundGoal):
            #List to hold final path
            finalPath = []
            #Print the total path
            print("Total path taken by DFS:" , totalPath)
            #We are going to look at everyone's parents
            node = currentNode
            # The last visited node is the end-node's parent, append it first
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
            print("Final path from start to end as found by DFS" , finalPath)
            if (self.GUI is not None):
                for node in finalPath[1:-1]:
                    time.sleep(float(1)/self.GUI.speed.get())
                    self.updatePlot(node, "blue")

        else:
            print(totalPath)
            print("Could Not Find Node")

