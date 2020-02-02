from Algorithm import *
import random
class Dijkstra_2(Algorithm):
    def __init__(self, graph, startNodeNumber, endNodeNumber):
            super().__init__(graph,startNodeNumber, endNodeNumber)
    def resetGraph(self):
        self.graph = Graph(nodesTall=self.graph.nodesTall, nodesWide=self.graph.nodesWide)
    def getNodeCost(self, node):
        #Arbitrarty heuristic so that cost to get to node is not uniform
        #Also, we want the cost to be different depending on the parent ;)
        random.seed(node.number)
        costToExplore = random.random() * 5
        #print("cost:", node.number, costToExplore)
        #Backtrack to the source to see the current
        #We are going to add the cost to traverse from the parent
        #In case we have some cheaper path through a different node
        while(node.parent != None):
            parentNodeCost = node.parent.costToExplore
            costToExplore += parentNodeCost
            node = node.parent
        # random.seed(node.parent.number)
        # parentNodeCost = random.random() * 3
        # costToExplore += parentNodeCost
        #return 1
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
        while(self.foundGoal != True and len(self.unVisited) != 0):
            currentNode = self.unVisited.pop(0)
            neighbors = self.graph.getNodeNeighbors(currentNode.number)
            currentNode.neighbors = neighbors
            totalPath.append(currentNode.number)
            #print("Visiting: " + str(currentNode.number))
            self.visited.append(currentNode.number)
            for n in neighbors:
                #if we haven't visited it or the cost to it has changed
                if(n in self.unVisited):
                    continue
                currentNeighborNode = self.graph.makeNodeFromNumber(n)
                costToExplore = self.getNodeCost(currentNeighborNode)
                #If one of the neighbors is the node we are looking for
                if n == self.endNodeNumber:
                    #print("Found node!")
                    self.foundGoal = True
                #If the new found cost is lower, we should revisit it
                if (costToExplore < currentNeighborNode.costToExplore):
                    currentNeighborNode.costToExplore = costToExplore
                    currentNeighborNode.parent = currentNode
                    #print("Adding to unvisited: " + str(n) + ", Parent is: " + str(currentNeighborNode.parent.number))
                    self.unVisited.append(currentNeighborNode)
            #sort the list
            self.unVisited.sort(key=lambda x: x.costToExplore)
            #[print(i.number, i.costToExplore) for i in self.unVisited]


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
            print("Final path from start to end as found by Dijkstra's:" , finalPath)

        else:
            print("Could Not Find Node")

