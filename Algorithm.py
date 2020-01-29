"""
Generic Algorithm Class that the search algorithms will inherit from
Has:
Run method (will be overwritten)
"""
from Node import *
from Graph import *
class Algorithm():
    def __init__(self, graph, startNodeNumber, endNodeNumber):
        self.graph = graph
        self.visited = []
        self.unVisited = []
        self.finalPath = []
        self.startNodeNumber = startNodeNumber
        self.endNodeNumber = endNodeNumber
    def run(self):
        pass
    def getPath(self):
        return self.finalPath