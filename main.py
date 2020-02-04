#TODO:
# 1) Obstacle avoid,
# 2) Make sure you have placed a start and end when hit run,
# 3) if start is (0,0), and place end, start disappears
# 4) Check if for text GUI valid nodes are chosen

from Graph import *
from BFS import *
from DFS import *
from Dijkstra_2 import *
from tkinter import *

class GUI():
    def __init__(self):
        self.win = Tk()
        self.win.title("RBE 550 Search Algorithms ")
        #self.win.attributes("-fullscreen", True)
        self.win.geometry('1000x700')
        self.win.configure(background="grey")
        self.canvas = Canvas(self.win, width=600, height=800, bg="grey", highlightthickness=0)

        self.startNode = 0
        self.endNode = 0
        self.g = Graph(nodesTall=10, nodesWide=10)
        # self.startIndexes = g.getNodeIndexes(startNode)
        # self.endIndexes = g.getNodeIndexes(endNode)
        self.selectingStart = False
        self.selectingEnd = False
        self.selectingObs = False
        self.deletingObs = False
        self.nodes = {}
        self.makeGrid(self.g.nodesTall, self.g.nodesWide)


    def makeGrid(self,nodesTall = 10, nodesWide = 10):
        self.g = Graph(nodesTall=10, nodesWide=10)
        self.startNode = 0
        self.endNode = 0
        for i in range(nodesTall):
            for j in range(nodesWide):
                number = self.g.getNodeNumber(i, j)
                self.nodes[number] = Button(self.win, height=3, width=6, command=lambda row=i, column=j: self.select(row, column), bg = "white")
                self.nodes[number].grid(row = i, column = j)

    def select(self,row, column):
        if(self.selectingStart):
            #Erasing old start node, by grabbing the coordinates of the start and setting that button to white
            startNodeCoord = self.g.getNodeIndexes(self.startNode)
            node = Button(self.win, height=3, width=6, command=lambda row=startNodeCoord[0],
                        column=startNodeCoord[1]: self.select(row, column),
                        bg="white")
            node.grid(row=startNodeCoord[0], column=startNodeCoord[1])
            #now place the new start where the user placed it and make it red
            node = Button(self.win, height=3, width=6, command=lambda row=row, column=column: self.select(row, column), bg="red",
                          state="disabled")
            node.grid(row=row, column=column)
            self.win.update()
            self.startNode = self.g.getNodeNumber(row,column)
            self.updateSelectStart()

        elif(self.selectingEnd):
            # Erasing old end node, by grabbing the coordinates of the start and setting that button to white
            endNodeCoord = self.g.getNodeIndexes(self.endNode)
            node = Button(self.win, height=3, width=6, command=lambda row=endNodeCoord[0],
                                                column=endNodeCoord[1]: self.select(row, column),
                                                bg="white")
            node.grid(row=endNodeCoord[0], column=endNodeCoord[1])
            # now place the new end where the user placed it and make it green
            node = Button(self.win, height=3, width=6, command=lambda row=row, column=column: self.select(row, column), bg="green",
                          state="disabled")
            node.grid(row=row, column=column)
            self.win.update()
            self.endNode = self.g.getNodeNumber(row, column)
            self.updateSelectEnd()
        else:
            node = Button(self.win, height=3, width=6, command=lambda row=row, column=column: self.select(row, column), bg = "black")
            node.grid(row=row, column=column)
            print(row, column)

    def updateSelectStart(self):
        if self.selectingStart == False:
            self.selectingStart = True
        elif self.selectingStart == True:
            self.selectingStart = False

    def updateSelectEnd(self):
        if self.selectingEnd == False:
            self.selectingEnd = True
        elif self.selectingEnd == True:
            self.selectingEnd = False

    def runSearchAlgorithm(self, alg):
        if alg.get() == "DFS":
            dfs = DFS(self.g,self.startNode, self.endNode, window = self.win)
            dfs.run()
        elif alg.get() == "BFS":
            bfs = BFS(self.g,self.startNode, self.endNode, window = self.win)
            bfs.run()
        else:
            dijkstra = Dijkstra_2(self.g, self.startNode, self.endNode, window = self.win)
            dijkstra.run()

    def homeScreen(self):
        selectStart = Button(self.win, height=3, width=8,  text = "Place Start", command=self.updateSelectStart)
        selectStart.grid(row = 3, column = 11)
        selectEnd = Button(self.win, height=3, width=8, text="Place End", command=self.updateSelectEnd)
        selectEnd.grid(row = 4, column = 11)
        reset = Button(self.win, height=3, width=8, text="Reset", command=self.makeGrid)
        reset.grid(row=5, column=11)
        # Create a Tkinter variable
        drop = StringVar(self.win)
        # Dictionary with options
        choices = ['BFS', 'DFS', 'Dijkstra']
        drop.set(choices[0])  # set the default option
        popupMenu = OptionMenu(self.win, drop, *choices)
        Label(text="Choose Search Algorithm").grid(row=1, column=11)
        popupMenu.grid(row=1, column=11, rowspan = 2)
        runAlgorithm = Button(self.win, height=3, width=12, text="Run",
                              command=lambda alg=drop: self.runSearchAlgorithm(drop))
        runAlgorithm.grid(row=11, column=4, columnspan=2)
        self.win.update()

if __name__ == '__main__':
    #Ask the user if they want a gui, if they do
    wantGui = input("Do you want to use the GUI? (y/n)")
    if wantGui == "y" or wantGui ==  "Y" or wantGui ==  "yes" or wantGui == "Yes" or wantGui == "YES":
        gui = GUI()
        gui.homeScreen()
        gui.win.mainloop()
    #otherwise:
    else:
        #TODO: Check if valid nodes
        startNode = input("What is your start node? (0 to 99)")
        startNode = int(startNode)
        endNode = input("What is your end node? (0 to 99)")
        endNode = int(endNode)
        alg = input("What algorithm do you want to use? (1: BFS, 2: DFS, 3: Dijkstra's)")
        g = Graph(nodesTall=10, nodesWide=10)
        while(alg not in ["1", "2", "3"]):
            alg = input("What algorithm do you want to use? (1: BFS, 2: DFS, 3: Dijkstra's)")
        if alg == "1":
            bfs = BFS(g, startNode, endNode)
            bfs.run()
        elif alg == "2":
            dfs = DFS(g, startNode, endNode)
            dfs.run()
        elif alg == "3":
            dijkstra = Dijkstra_2(g, startNode, endNode)
            dijkstra.run()