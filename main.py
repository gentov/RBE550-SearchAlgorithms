#TODO by 2/20:
# 1) Won't backtrack with obstacles --> I think done
# 2) Obstacle avoid --> Works, but I don't love it.
# 3) Make sure you have placed a start and end when hit run
# 4) if start is (0,0), and place end, start disappears --> I think done
# 5) Check if for text GUI valid nodes are chosen
# 6) Pad it so that the grid isn't just in the top left corner --> Done
# 7) Turtle
# 8) Implement the other algorithms (A* and WA*) --> I think done
# 9) Let user choose four connected or 8 connected
# 10) Bug with reset sometimes

from Graph import *
from BFS import *
from DFS import *
from Dijkstra_2 import *
from tkinter import *
from A_Star import *
from WA_Star import *
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen

class GUI():
    def __init__(self):
        self.win = Tk()
        self.win.title("RBE 550 Search Algorithms ")
        #self.win.attributes("-fullscreen", True)
        self.win.geometry('1000x700')
        self.win.configure(background="grey")
        self.canvas = Canvas(self.win, width=700, height=800, bg="grey", highlightthickness=0)

        self.startNode = None
        self.endNode = None
        self.blocked = []
        self.g = Graph(nodesTall=25, nodesWide=30)
        # self.startIndexes = g.getNodeIndexes(startNode)
        # self.endIndexes = g.getNodeIndexes(endNode)
        self.selectingStart = False
        self.selectingEnd = False
        self.selectingObs = False
        self.deletingObs = False
        self.fourConnected = IntVar()
        self.nodes = {}
        #This is the frame for the grid
        self.gridFrame = Frame(self.win)
        self.gridFrame.place(relx = .05, rely = .05)
        #This is a frame for buttons to the right of the grid
        self.buttonFrame = Frame(self.win, bg = "grey")
        self.buttonFrame.place(relx=.79, rely=.2)
        self.makeGrid(self.g.nodesTall, self.g.nodesWide)
        self.speed = None


    def makeGrid(self,nodesTall = 25, nodesWide = 30):
        self.g = Graph(nodesTall=nodesTall, nodesWide=nodesWide)
        self.startNode = None
        self.endNode = None
        self.blocked = []
        for i in range(nodesTall):
            for j in range(nodesWide):
                number = self.g.getNodeNumber(i, j)
                self.nodes[number] = Button(self.gridFrame, height=1, width=2,
                                            command=lambda number = number: self.select(number), bg = "white")
                self.nodes[number].grid(row = i, column = j)

    def resetGrid(self,nodesTall = 25, nodesWide = 30):
        self.g = Graph(nodesTall=nodesTall, nodesWide=nodesWide)
        self.startNode = None
        self.endNode = None
        self.blocked = []
        for i in range(nodesTall):
            for j in range(nodesWide):
                number = self.g.getNodeNumber(i, j)
                self.nodes[number].configure(bg = "white")

    def select(self, number):
        if(self.selectingStart):
            if(self.startNode is not None):
                #Erasing old start node, by grabbing the old start and setting that button to white
                oldNode = self.nodes[self.startNode].configure(bg="white")
            #now place the new start where the user placed it and make it red
            newnode = self.nodes[number].configure(bg="red")
            self.win.update()
            self.startNode = number #self.g.getNodeNumber(row,column)
            self.updateSelectStart()

        elif(self.selectingEnd):
            if(self.endNode is not None):
                # Erasing old end node, by grabbing the old end and setting that button to white
                oldNode = self.nodes[self.endNode].configure(bg="white")
            # now place the new start where the user placed it and make it red
            newNode = self.nodes[number].configure(bg="green")
            self.win.update()
            self.endNode = number
            self.updateSelectEnd()
        else:
            # Placing an obstable
            obstable = self.nodes[number].configure(bg="black")
            self.win.update()
            self.blocked.append(number)

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
            dfs = DFS(self.g,self.startNode, self.endNode, GUI = self)
            dfs.run()
        elif alg.get() == "BFS":
            bfs = BFS(self.g,self.startNode, self.endNode, GUI = self)
            bfs.run()
        elif alg.get() == "A*":
            a_star = A_Star(self.g, self.startNode, self.endNode, GUI = self)
            a_star.run()
        elif alg.get() == "WA*":
            wa_star = WA_Star(self.g, self.startNode, self.endNode, GUI = self)
            wa_star.run()
        else:
            dijkstra = Dijkstra_2(self.g, self.startNode, self.endNode, GUI=self)
            dijkstra.run()
    def homeScreen(self):
        drop = StringVar(self.buttonFrame)
        # Dictionary with options
        choices = ['BFS', 'DFS', 'Dijkstra', 'A*', 'WA*']
        drop.set(choices[0])  # set the default option
        popupMenu = OptionMenu(self.buttonFrame, drop, *choices)
        Label(self.buttonFrame, text="Choose Search Algorithm").grid(row=0, column=1)
        popupMenu.grid(row=1, column=1, rowspan=2, pady = 5)
        fourConnect = Checkbutton(self.buttonFrame, text="Four Connected", variable=self.fourConnected)
        fourConnect.grid(row=3, column=1, pady=10)
        selectStart = Button(self.buttonFrame, height=3, width=8,  text = "Place Start", command=self.updateSelectStart)
        selectStart.grid(row = 4, column = 1, pady = 5)
        selectEnd = Button(self.buttonFrame, height=3, width=8, text="Place End", command=self.updateSelectEnd)
        selectEnd.grid(row = 5, column = 1,pady = 5)
        reset = Button(self.buttonFrame, height=3, width=8, text="Reset", command=self.resetGrid)
        reset.grid(row=6, column= 1, pady = 5)
        # Create a Tkinter variable
        runAlgorithm = Button(self.buttonFrame, height=3, width=12, text="Run",
                              command=lambda alg=drop: self.runSearchAlgorithm(drop))
        runAlgorithm.grid(row=7, column=1, pady = 20)
        Label(self.buttonFrame, text="Speed").grid(row=3, column=2, rowspan = 2)
        self.speed = Scale(self.buttonFrame, from_= 100, to = 1)
        self.speed.set(50)
        self.speed.grid(row = 4, column = 2, rowspan = 2, pady = 40)

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
        while(alg not in ["1", "2", "3", "4", "5"]):
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
        elif alg == "4":
            a_star = A_Star(g, startNode, endNode)
            a_star.run()
        elif alg == "5":
            wa_star = WA_Star(g, startNode, endNode)
            wa_star.run()