from Graph import *
from BFS import *
from DFS import *
from Dijkstra_2 import *
from tkinter import *

win = Tk()
win.title("RBE 550 Search Algorithms ")
#win.attributes("-fullscreen", True)
win.geometry('600x450')
f = Frame(win)
f.place(relx=0.5, rely=0.5, anchor=CENTER)
win.configure(background="grey")
canvas = Canvas(win, width=600, height=800, bg="grey", highlightthickness=0)

startNode = 0
endNode = 0
g = Graph(nodesTall=10, nodesWide=10)
startIndexes = g.getNodeIndexes(startNode)
endIndexes = g.getNodeIndexes(endNode)
selectingStart = False
selectingEnd = False
selectingObs = False
deletingObs = False
def makeGrid(nodesTall, nodesWide):
   nodeNumber = 0
   for i in range(nodesTall):
       for j in range(nodesWide):
           node = Button(win, height=3, width=6, command=lambda row=i, column=j: select(row, column))
           node.grid(row = i, column = j)
           nodeNumber+=1

def updateStart(row, col):
     node = Button(win, height=3, width=6, command=lambda row=row, column=col: select(row, column), bg="red",
                   state = "disabled")
     node.grid(row=row, column=col)
     win.update()

def updateEnd(row, col):
     node = Button(win, height=3, width=6, command=lambda row=row, column=col: select(row, column), bg="green",
                   state = "disabled")
     node.grid(row=row, column=col)
     win.update()

def select(row, column):
    global startNode
    global endNode
    if(selectingStart):
        node = Button(win, height=3, width=6, command=lambda row=row, column=column: select(row, column), bg="red",
                      state="disabled")
        node.grid(row=row, column=column)
        win.update()
        startNode = g.getNodeNumber(row,column)
        print(startNode)
        updateSelectStart()
    elif(selectingEnd):
        node = Button(win, height=3, width=6, command=lambda row=row, column=column: select(row, column), bg="green",
                      state="disabled")
        node.grid(row=row, column=column)
        win.update()
        endNode = g.getNodeNumber(row, column)
        updateSelectEnd()
    else:
        node = Button(win, height=3, width=6, command=lambda row=row, column=column: select(row, column), bg = "black")
        node.grid(row=row, column=column)
        print(row, column)
def updateSelectStart():
    global selectingStart
    print(selectingStart)
    if selectingStart == False:
        selectingStart = True
    elif selectingStart == True:
        selectingStart = False

def updateSelectEnd():
    global selectingEnd
    if selectingEnd == False:
        selectingEnd = True
    elif selectingEnd == True:
        selectingEnd = False

def runSearchAlgorithm():
    #dfs = DFS(g,startNode, endNode, window = win)
    #bfs = BFS(g,startNode, endNode, window = win)
    dijkstra = Dijkstra_2(g, startNode, endNode, window = win)
    #Algorithms = [bfs, dfs, dijkstra]
    #bfs.run()
    dijkstra.run()

def homeScreen():
    selectStart = Button(win, height=3, width=8,  text = "Place Start", command=updateSelectStart)
    selectStart.place(relx = .4, rely = .2)
    selectEnd = Button(win, height=3, width=8, text="Place End", command=updateSelectEnd)
    selectEnd.place(relx=.4, rely=.3)
    runAlgorithm = Button(win, height=3, width=8, text="Run", command=runSearchAlgorithm)
    runAlgorithm.place(relx=.4, rely=.5)
    makeGrid(g.nodesTall, g.nodesWide)
    #updateStart(startIndexes[0], startIndexes[1])
    #updateEnd(endIndexes[0], endIndexes[1])

homeScreen()
win.mainloop()



#for a in Algorithms:
#     a.run()
#     print("")