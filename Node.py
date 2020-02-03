"""
What does a Node need?:
Neighbors
Parents
(We can make the following optional)
A Width (Assuming we have a grid)
A Height (assuming we have a grid)
"""
import sys
class Node():
    def __init__(self, row = None, column = None, number = None):
        self.isGoal = False
        if(column is not None and row is not None):
            self.row = row
            self.column = column
        if(number is not None):
            self.number = number
        self.parent = None
        self.neighbors = [None]*4
        self.costToExplore = sys.maxsize
    def getNeighbors(self):
        return self.neighbors
    def getParents(self):
        #parents are those nodes that are explored before this one
        pass
