from Graph import *
from BFS import *
from DFS import *

g = Graph()
startNode = 5
endNode = 15
Algorithms = [DFS(g, startNode, endNode),BFS(g, startNode, endNode)]
for a in Algorithms:
    a.run()
    print("")