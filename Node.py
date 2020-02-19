"""
What does a Node need?:
Neighbors
Parents
"""
import sys
class Node():
    def __init__(self, row = None, column = None, number = None, x = None, y = None):
        self.isGoal = False
        if(column is not None and row is not None):
            self.row = row
            self.column = column
        if(number is not None):
            self.number = number
        self.parent = None
        self.neighbors = [None]*4
        self.costToExplore = sys.maxsize
        self.totalCost = sys.maxsize
        if(x is not None and y is not None):
            self.x = x
            self.y = y
    def getNeighbors(self):
        return self.neighbors
    def getParents(self):
        #parents are those nodes that are explored before this one
        pass
