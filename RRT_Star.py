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
        self.expandDistance = 20
        self.win = Tk()
        self.speed = 100
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
                print("Smallest Distance: ", smallestDistance)

        return nearestNode

    def calculateDistance(self, node1, node2):
        return(math.sqrt((abs(node1.x - node2.x)**2) + (abs(node1.y - node2.y)**2)))

    def checkCollision(self, node):
        return 0

    def drawPoint(self, x, y, color):
        self.canvas.create_oval(x - 5,y - 5,x+5,y+5, fill = color)

    def connect(self, randomNode, nearestNode, color = None):
        # instead of connecting directly, every 5 pixels, place a new node along the line, and check for obstacle
        # find vector put points on it
        parent = nearestNode
        newNode = randomNode
        distance = 10
        # if we are really close from the start, no need to go on.
        if (self.calculateDistance(newNode, parent) < distance):
            self.drawPoint(newNode.x, newNode.y, color='blue')
            # connect parent and new node
            self.canvas.create_line(parent.x, parent.y, newNode.x, newNode.y)
            self.drawPoint(newNode.x, newNode.y, color='blue')
            newNode.parent = parent
            self.nodes.append(newNode)
            return

        yDiff = newNode.y - parent.y
        xDiff = newNode.x - parent.x
        angle = math.atan2(yDiff, xDiff)
        xIncrement = distance*math.cos(angle)
        yIncrement = distance*math.sin(angle)
        newNodeInLine = Node(x = parent.x + xIncrement, y = parent.y + yIncrement)
        newNodeInLine.parent = parent

        while(self.calculateDistance(newNodeInLine, newNode) > distance):
            # create a node
            if(not self.checkCollision(newNodeInLine)):
                # append it to the node list
                self.nodes.append(newNodeInLine)
                #draw the node
                self.drawPoint(newNodeInLine.x, newNodeInLine.y, color = 'blue')
                # draw a line between the previous one and the new one
                self.canvas.create_line(newNodeInLine.x, newNodeInLine.y, parent.x, parent.y)
                # the new node becomes the parent
                parent = newNodeInLine
                # make a new node on the line
                newNodeInLine = Node(x = parent.x + xIncrement, y = parent.y + yIncrement)
                # set the parent of the new node to the previous one on the line
                newNodeInLine.parent = parent
            else:
                break
        #if we are close to the original new node
        if(self.calculateDistance(newNodeInLine, newNode) < distance):
            self.drawPoint(newNodeInLine.x, newNodeInLine.y, color='blue')
            # draw a line between the last one on the line and the new one on the line
            self.canvas.create_line(newNodeInLine.parent.x, newNodeInLine.parent.y, newNodeInLine.x, newNodeInLine.y)
            self.drawPoint(newNode.x, newNode.y, color='blue')
            newNode.parent = newNodeInLine
            # draw a line between the last one in the line and the original point we made
            self.canvas.create_line(newNodeInLine.x, newNodeInLine.y, newNode.x, newNode.y)
            #append it to the list of nodes we have
            self.nodes.append(newNode)

    def directConnect(self, newNode, parent, color = None):
        #Directly draw a line between two nodes, do not put nodes in between them
        self.canvas.create_line(newNode.x, newNode.y, parent.x, parent.y, fill = color, width = 10)

    def drawFinalPath(self):
        node = endNode
        while(node.parent is not None):
            self.directConnect(node, node.parent, color = 'green')
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
            #I think the following line is taken care of in connect
            # randomNode.parent = nearestNode
            # print("Parent to new node set")
            self.connect(randomNode, nearestNode)

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