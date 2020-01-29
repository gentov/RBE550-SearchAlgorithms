from Node import *
class Graph():
    def __init__(self, nodesTall = 4 ,nodesWide = 4):
        self.nodesTall = nodesTall
        self.nodesWide = nodesWide
        self.graph = [[0 for i in range(nodesWide)] for j in range(nodesTall)]
        self.makeGraph()

    def makeGraph(self):
        nodeNumber = 0
        for i in range(self.nodesTall):
            for j in range(self.nodesWide):
                self.graph[i][j] = Node(number=nodeNumber)
                nodeNumber+=1

    def print(self):
        for i in range(self.nodesTall):
            for j in range(self.nodesWide):
                print(i,j,self.graph[i][j].number)

    def getNodeIndexes(self, nodeNumber):
        row = int(nodeNumber/self.nodesWide)
        column = nodeNumber % self.nodesWide
        return [row, column]

    def getNodeNumber(self, row, column):
        number = row*self.nodesWide + column%self.nodesWide
        return number

    def getNodeNeighbors(self, nodeNumber):
        # N,E,S,W
        neighbors = []
        row = self.getNodeIndexes(nodeNumber)[0]
        column = self.getNodeIndexes(nodeNumber)[1]
        #If we have neighbors to the north
        if(row > 0):
            neighbors.append(self.graph[row - 1][column].number)
        # If we have neighbors to the east
        if (column < self.nodesWide - 1):
            neighbors.append(self.graph[row][column + 1].number)
        # If we have neighbors to the south
        if (row < self.nodesTall - 1):
            neighbors.append(self.graph[row + 1][column].number)
        # If we have neighbors to the west
        if (column > 0):
            neighbors.append(self.graph[row][column - 1].number)

        return neighbors

    def makeNodeFromNumber(self, nodeNumber):
        # Grab the indexes of that node so we can get our node object
        nodeIndexes = self.getNodeIndexes(nodeNumber)
        # we have our node object
        madeNode = self.graph[nodeIndexes[0]][nodeIndexes[1]]
        return madeNode
