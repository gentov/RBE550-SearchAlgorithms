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

def homeScreen():
     node = Button(f,bg='yellow green', font=("Verdana", 18), height=5, width=5)

def makeGrid(nodesTall, nodesWide):
   nodeNumber = 0
   for i in range(nodesTall):
       for j in range(nodesWide):
           node = Button(win, height=3, width=6, command=lambda row=i, column=j: select(row, column))
           node.grid(row = i, column = j)
           nodeNumber+=1
def updateStart(row, col):
     node = Button(win, height=3, width=6, command=lambda row=row, column=col: select(row, column), bg="red")
     node.grid(row=row, column=col)
     win.update()
def updateEnd(row, col):
     node = Button(win, height=3, width=6, command=lambda row=row, column=col: select(row, column), bg="green")
     node.grid(row=row, column=col)
     win.update()
def select(row, column):
     node = Button(win, height=3, width=6, command=lambda row=row, column=column: select(row, column), bg = "black")
     node.grid(row=row, column=column)
     print(row, column)


startNode = 6
endNode = 40
g = Graph(nodesTall=10, nodesWide=10)
startIndexes = g.getNodeIndexes(startNode)
endIndexes = g.getNodeIndexes(endNode)
makeGrid(g.nodesTall, g.nodesWide)
updateStart(startIndexes[0],startIndexes[1])
updateEnd(endIndexes[0], endIndexes[1])

#dfs = DFS(g,startNode, endNode, window = win)
bfs = BFS(g,startNode, endNode, window = win)
#dijkstra = Dijkstra_2(g, startNode, endNode, window = win)
#Algorithms = [bfs, dfs, dijkstra]
bfs.run()
win.mainloop()
#for a in Algorithms:
#     a.run()
#     print("")