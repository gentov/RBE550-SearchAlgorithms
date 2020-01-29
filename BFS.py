from Algorithm import *
class BFS(Algorithm):
    def run(self):
        totalPath = []
        """
         PseduoCode for BFS:
            We mark the first node as unvisited
            then we explore the neighbors of that node, and add each one to the unvisited queue
            we have now explored the current node, so we add it to the visited queue
            We repeatedly pop the top element of the unvisited list and repeat until we reach the goal
        """
        initialNode = self.startNodeNumber
        #We mark the first node as unvisited
        self.unVisited.append(initialNode)
        #we have our current node object
        currentNode = self.graph.makeNodeFromNumber(initialNode)
        while(currentNode.number != self.endNodeNumber and len(self.unVisited) != 0):
            currentNodeNumber = self.unVisited.pop(0)
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
                self.unVisited.append(n)

        #If we have found the node
        if(currentNode.number == self.endNodeNumber):
            #List to hold final path
            finalPath = []
            #Print the total path
            print(totalPath)
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
            print(finalPath)


        else:
            print("Could Not Find Node")

