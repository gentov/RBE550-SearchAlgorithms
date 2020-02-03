"""
Generic Algorithm Class that the search algorithms will inherit from
Has:
Run method (will be overwritten)
"""
from Node import *
from Graph import *
from tkinter import *

class Algorithm():
    def __init__(self,graph,startNodeNumber, endNodeNumber, window = None):
        self.visited = []
        self.unVisited = []
        self.finalPath = []
        self.startNodeNumber = startNodeNumber
        self.endNodeNumber = endNodeNumber
        self.foundGoal = False
        self.graph = graph
        if(window is not None):
            self.win = window
        else:
            self.win = None

    def updatePlot(self, row, col,color):
        node = Button(self.win, height=3, width=6, bg=color, state="disabled")
        node.grid(row=row, column=col)
        self.win.update()

    def run(self):
        pass
    def getPath(self):
        return self.finalPath