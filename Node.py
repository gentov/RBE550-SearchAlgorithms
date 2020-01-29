"""
What does a Node need?:
Neighbors
Parents
(We can make the following optional)
A Width (Assuming we have a grid)
A Height (assuming we have a grid)
"""

class Node():
    def __init__(self, width = None, height = None, number = None):
        self.isGoal = False
        if(width is not None and height is not None):
            self.width = width
            self.height = height
        if(number is not None):
            self.number = number
        self.parent = None
        self.neighbors = [None]*4
    def getNeighbors(self):
        return self.neighbors
    def getParents(self):
        #parents are those nodes that are explored before this one
        pass
