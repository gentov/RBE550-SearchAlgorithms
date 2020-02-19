import time
import random
import sys
import math
from Node import *
from tkinter import *

class RRT_Star():
    def __init__(self, startNode, endNode, GUI = None):
        self.visited = []
        self.unVisited = []
        self.finalPath = []
        self.startNode= startNode
        self.endNode = endNode
        self.maxIterations = 5000
        self.foundGoal = False
        self.nodes = []
        self.expandDistance = 10
        self.win = Tk()
        self.speed = 80
        self.win.geometry('700x800')
        self.win.configure(background="grey")
        self.win.title("Test")
        self.canvas = Canvas(self.win, width=700, height=800, bg="grey", highlightthickness=0)
        self.canvas.pack()

        if (GUI is not None):
            self.GUI = GUI
        else:
            self.GUI = None
    def generateRandomNode(self):
        randomNodeX = random.randint(10, 700)
        randomNodeY = random.randint(10, 800)
        newNode = Node(x = randomNodeX, y = randomNodeY)

        return newNode

    def getNearestNode(self, newNode):
        # return nearest node to given node in node list
        smallestDistance = self.calculateDistance(newNode, startNode)
        nearestNode = self.nodes[0]
        for i in range(len(self.nodes)):
            distance = self.calculateDistance(self.nodes[i], newNode)
            if(distance < smallestDistance):
                nearestNode = self.nodes[i]
                smallestDistance = distance

        return nearestNode

    def calculateDistance(self, node1, node2):
        return(math.sqrt((abs(node1.x - node2.x)**2) + (abs(node1.y - node2.y)**2)))

    def checkCollision(self, node):
        return 0

    def drawPoint(self, x, y, color):
        self.canvas.create_oval(x - 5,y - 5,x+5,y+5, fill = color)

    def connect(self, newNode, parent, color = None):
        if(color is None):
            self.canvas.create_line(newNode.x, newNode.y, parent.x, parent.y)
        else:
            self.canvas.create_line(newNode.x, newNode.y, parent.x, parent.y, width = 8, fill = color)

    def drawFinalPath(self):
        node = endNode
        while(node.parent is not None):
            self.connect(node, node.parent, color = 'green')
            time.sleep(1/self.speed)
            node = node.parent
            self.win.update()
        self.win.mainloop()

    def run(self):
        self.foundGoal = False
        totalPath = []

        """
         PseduoCode for RRT:
         Points are randomly generated and connected to the closest available node. 
         Each time a vertex is created, a check must be made that the vertex lies outside of an obstacle. 
         Furthermore, chaining the vertex to its closest neighbor must also avoid obstacles. 
         The algorithm ends when a node is generated within the goal region, or a limit is hit.
         source:https://medium.com/@theclassytim/robotic-path-planning-rrt-and-rrt-212319121378
        """
        self.nodes.append(self.startNode)
        self.drawPoint(startNode.x, startNode.y, 'red')
        self.drawPoint(endNode.x, endNode.y, 'green')
        for i in range(self.maxIterations):
            #create random node
            randomNode = self.generateRandomNode()
            print("Random Node Created at: ", randomNode.x, randomNode.y)
            #find closest node in list and return it
            nearestNode = self.getNearestNode(randomNode)
            print("Nearest Node to New Node at Coordinates:", nearestNode.x, nearestNode.y)
            randomNode.parent = nearestNode
            print("Parent to new node set")
            self.connect(randomNode, nearestNode)

            if(self.checkCollision(randomNode) == 0):
                print("Added new Node to list")
                self.nodes.append(randomNode)
                self.drawPoint(randomNode.x, randomNode.y, 'blue')

            distanceToGoal = self.calculateDistance(self.nodes[-1], self.endNode)
            if(distanceToGoal <= self.expandDistance):
                print("Found Goal")
                self.foundGoal = True
                self.endNode.parent = self.nodes[-1]
                self.drawFinalPath()
            time.sleep(1/self.speed)
            self.win.update()
        if(not self.foundGoal):
            print("Could Not Find Goal")

startNode = Node(x = 10, y = 10)
endNode = Node(x = 690, y = 790)
rrt = RRT_Star(startNode, endNode)
rrt.win.update()
rrt.run()