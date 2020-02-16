
from A_Star import *
class WA_Star(A_Star):
    def __init__(self, graph, startNodeNumber, endNodeNumber, GUI = None):
            super().__init__(graph,startNodeNumber, endNodeNumber, GUI)
            self.weight = 5
    def resetGraph(self):
        self.graph = Graph(nodesTall=self.graph.nodesTall, nodesWide=self.graph.nodesWide)

    # #Change get edge cost for 8 connected
    def getHeuristic(self, neighborNode):
        # get estimated distance to goal
        (row, col) = self.graph.getNodeIndexes(neighborNode.number)
        (rowEnd,colEnd) = self.graph.getNodeIndexes(self.endNodeNumber)
        heuristicValue = (abs(row - rowEnd)) + (abs(col - colEnd))
        print("Neighbor Node: ", neighborNode.number, "Heuristic: ", heuristicValue)
        return heuristicValue * self.weight
