"""
Generic Algorithm Class that the search algorithms will inherit from
Has:
Run method (will be overwritten)
"""
from Node import *
from Graph import *
from tkinter import *

class Algorithm():
    def __init__(self,graph,startNodeNumber, endNodeNumber, GUI = None):
        self.visited = []
        self.unVisited = []
        self.finalPath = []
        self.startNodeNumber = startNodeNumber
        self.endNodeNumber = endNodeNumber
        self.foundGoal = False
        self.graph = graph
        if(GUI is not None):
            self.GUI = GUI
        else:
            self.GUI = None

    def updatePlot(self, number, color):
        self.GUI.nodes[number].configure(bg=color)
        self.GUI.win.update()

    def run(self):
        pass
    def getPath(self):
        return self.finalPath