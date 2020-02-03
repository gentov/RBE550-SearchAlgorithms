from Graph import *
from BFS import *
from DFS import *
from Dijkstra_2 import *
from tkinter import *

class GUI():
    def __init__(self):
        self.win = Tk()
        self.win.title("RBE 550 Search Algorithms ")
        #win.attributes("-fullscreen", True)
        self.win.geometry('600x450')
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
    def makeGrid(self,nodesTall, nodesWide):
       nodeNumber = 0
       for i in range(nodesTall):
           for j in range(nodesWide):
               node = Button(self.win, height=3, width=6, command=lambda row=i, column=j: self.select(row, column))
               node.grid(row = i, column = j)
               nodeNumber+=1

    def updateStart(self,row, col):
         node = Button(win, height=3, width=6, command=lambda row=row, column=col: self.select(row, column), bg="red",
                       state = "disabled")
         node.grid(row=row, column=col)
         self.win.update()

    def updateEnd(self,row, col):
         node = Button(self.win, height=3, width=6, command=lambda row=row, column=col: self.select(row, column), bg="green",
                       state = "disabled")
         node.grid(row=row, column=col)
         self.win.update()

    def select(self,row, column):
        if(self.selectingStart):
            node = Button(self.win, height=3, width=6, command=lambda row=row, column=column: self.select(row, column), bg="red",
                          state="disabled")
            node.grid(row=row, column=column)
            self.win.update()
            self.startNode = self.g.getNodeNumber(row,column)
            self.updateSelectStart()
        elif(self.selectingEnd):
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

    def runSearchAlgorithm(self):
        #dfs = DFS(g,startNode, endNode, window = win)
        bfs = BFS(self.g,self.startNode, self.endNode, window = self.win)
        #dijkstra = Dijkstra_2(self.g, self.startNode, self.endNode, window = self.win)
        #Algorithms = [bfs, dfs, dijkstra]
        bfs.run()
        #dijkstra.run()

    def homeScreen(self):
        selectStart = Button(self.win, height=3, width=8,  text = "Place Start", command=self.updateSelectStart)
        selectStart.place(relx = .4, rely = .2)
        selectEnd = Button(self.win, height=3, width=8, text="Place End", command=self.updateSelectEnd)
        selectEnd.place(relx=.4, rely=.3)
        self.runAlgorithm = Button(self.win, height=3, width=8, text="Run", command=self.runSearchAlgorithm)
        self.runAlgorithm.place(relx=.4, rely=.5)
        self.makeGrid(self.g.nodesTall, self.g.nodesWide)
        #updateStart(startIndexes[0], startIndexes[1])
        #updateEnd(endIndexes[0], endIndexes[1])

gui = GUI()
gui.homeScreen()
gui.win.mainloop()



    #for a in Algorithms:
    #     a.run()
    #     print("")