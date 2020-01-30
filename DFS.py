
from Algorithm import *
class DFS(Algorithm):
    def run(self):
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
        #We mark the first node as unvisited
        self.unVisited.append(initialNode)
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        #stack.append(currentNode.number)
        while(currentNode.number != self.endNodeNumber and len(self.unVisited) != 0):
            #pop the unvisited node off the top
            # currentNodeNumber = stack.pop(0)
            currentNodeNumber = self.unVisited.pop(0)
            #print("Visiting: ", currentNodeNumber)
            currentNode = self.graph.makeNodeFromNumber(currentNodeNumber)
            neighbors = self.graph.getNodeNeighbors(currentNodeNumber)
            #print("Node Neighbors are: ", neighbors)
            currentNode.neighbors = neighbors
            #this node has no neighbors, so our current node becomes the current node's parent
            if len(neighbors) == 0:
             #   print(currentNodeNumber, " has no neighbors.")
                currentNode = currentNode.parent
                continue
            #append the current node to the total path
            totalPath.append(currentNode.number)
            #add the current node to the visited list
            self.visited.append(currentNode.number)
            #Append to the unvisited array (our stack), the first neighbor we explore, and then break
            for i in range(len(neighbors)):
                if(neighbors[i] not in self.visited):
                    currentNeighborNode = self.graph.makeNodeFromNumber(neighbors[i])
                    currentNeighborNode.parent = currentNode
                    self.unVisited.append(neighbors[i])
                    nextNodeToVisit = neighbors[i]
                    break
                #If you have iterated through all the nodes and we have visited them all, backtrack one:
                if(i == len(neighbors) - 1):
                    nextNodeToVisit = currentNode.parent.number
            #check if we have returned to the start OR we have been stuck on the same node
            if(nextNodeToVisit == initialNode): # or nextNodeToVisit == currentNode.number):
              #  print("Next node to visit is: ", nextNodeToVisit, ". Returned to the start.")
                break
            print("Next node to visit: ", nextNodeToVisit)

        #If we have found the node
        if(currentNode.number == self.endNodeNumber):
            #List to hold final path
            finalPath = []
            #Print the total path
            print("Total path taken by DFS:" , totalPath)
            #We are going to look at everyone's parents
            node = currentNode
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
            print("Final path taken by DFS:" , finalPath)


        else:
            print(totalPath)
            print("Could Not Find Node")

