
from A_Star import *
"""
WA* inherits from A*, and changes the heuristic weight so that the algorithm puts more
emphasis on the heuristic instead of edge costs
"""
class WA_Star(A_Star):
    def __init__(self, graph, startNodeNumber, endNodeNumber, weight = 5, GUI = None):
            super().__init__(graph,startNodeNumber, endNodeNumber, GUI)
            self.weight = weight
    def resetGraph(self):
        self.graph = Graph(nodesTall=self.graph.nodesTall, nodesWide=self.graph.nodesWide)

    #
    def getHeuristic(self, neighborNode):
        # get estimated distance to goal
        (row, col) = self.graph.getNodeIndexes(neighborNode.number)
        (rowEnd,colEnd) = self.graph.getNodeIndexes(self.endNodeNumber)
        heuristicValue = (abs(row - rowEnd)) + (abs(col - colEnd))
        print("Neighbor Node: ", neighborNode.number, "Heuristic: ", heuristicValue*self.weight)
        return heuristicValue * self.weight
