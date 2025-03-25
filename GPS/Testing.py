import math
import networkx as nx
import matplotlib.pyplot as plt

nodeMap = {"Aquatic-Beak" : [452, 29], "Aquatic-Feather" : [305, 29], "Aquatic-Waddle" : [129, 29], "Aquatic-Waterfoul" : [213, 29],
           "Breadcrumb-Circle" : [284, 393], "Breadcrumb-Waddle": [181, 459], "Circle-Feather" : [305, 296], "Circle-Waterfoul" : [273, 307],
           "Dabbler-Beak" : [452, 293], "Dabbler-Circle" : [350, 324], "Dabbler-Mallard" : [585, 293],
           "Drake-Beak" : [452, 402], "Drake-Mallard" : [576, 354], "Duckling-Beak" : [452, 474], "Duckling-Mallard" : [593, 354],
           "Migration-Beak" : [452, 135], "Migration-Feather" : [305, 135], "Migration-Mallard" : [585, 135],
           "Migration-Quack" : [29, 135], "Migration-Waddle" : [129, 135], "Migration-Waterfoul" : [213, 135],
           "Pondside-Beak" : [452, 233], "Pondside-Feather" : [305, 233], "Pondside-Mallard" : [585, 233],
           "Pondside-Quack" : [28, 329], "Pondside-Waterfoul" : [214, 241], "Pondside-Waddle" : [157, 266],
           "Tail-Beak" : [452, 465], "Tail-Circle" : [335, 387]}

# Make graph
Graph = nx.DiGraph()

# Add nodes to graph
for node, position in nodeMap.items():
    Graph.add_node(node, pos = position)

Graph.add_edge("Pondside-Waddle", "Pondside-Quack")
Graph.add_edge("Pondside-Quack", "Pondside-Waddle")
Graph.add_edge("Pondside-Quack", "Breadcrumb-Waddle")
Graph.add_edge("Breadcrumb-Waddle", "Pondside-Quack")
Graph.add_edge("Migration-Waddle", "Migration-Quack")
Graph.add_edge("Migration-Quack", "Migration-Waddle")
Graph.add_edge("Migration-Quack", "Pondside-Quack")
Graph.add_edge("Pondside-Quack", "Migration-Quack")
Graph.add_edge("Migration-Waddle", "Migration-Waterfoul")
Graph.add_edge("Migration-Waterfoul", "Migration-Waddle")
Graph.add_edge("Migration-Quack", "Aquatic-Waddle")
Graph.add_edge("Aquatic-Waddle", "Migration-Quack")
Graph.add_edge("Migration-Waddle", "Aquatic-Waddle")
Graph.add_edge("Aquatic-Waterfoul", "Aquatic-Waddle")
Graph.add_edge("Aquatic-Waddle", "Aquatic-Waterfoul")
Graph.add_edge("Aquatic-Waterfoul", "Aquatic-Feather")
Graph.add_edge("Aquatic-Feather", "Aquatic-Waterfoul")
Graph.add_edge("Aquatic-Waterfoul", "Migration-Waterfoul")
Graph.add_edge("Pondside-Waddle", "Migration-Waddle")
Graph.add_edge("Breadcrumb-Waddle", "Pondside-Waddle")
Graph.add_edge("Migration-Waterfoul", "Pondside-Waterfoul")
Graph.add_edge("Pondside-Waterfoul", "Pondside-Waddle")
Graph.add_edge("Pondside-Waddle", "Pondside-Waterfoul")
Graph.add_edge("Aquatic-Feather", "Aquatic-Beak")
Graph.add_edge("Aquatic-Beak", "Aquatic-Feather")
Graph.add_edge("Migration-Mallard", "Aquatic-Beak")
Graph.add_edge("Aquatic-Beak", "Migration-Mallard")
Graph.add_edge("Migration-Mallard", "Migration-Beak")
Graph.add_edge("Migration-Beak", "Migration-Mallard")
Graph.add_edge("Aquatic-Beak", "Migration-Beak")
Graph.add_edge("Migration-Beak", "Aquatic-Beak")
Graph.add_edge("Migration-Feather", "Migration-Beak")
Graph.add_edge("Migration-Beak", "Migration-Feather")

Graph.add_edge("Migration-Feather", "Migration-Waterfoul")
Graph.add_edge("Migration-Waterfoul", "Migration-Feather")
Graph.add_edge("Aquatic-Feather", "Migration-Feather")
Graph.add_edge("Migration-Feather", "Aquatic-Feather")

Graph.add_edge("Migration-Feather", "Pondside-Feather")
Graph.add_edge("Pondside-Feather", "Migration-Feather")

Graph.add_edge("Pondside-Feather", "Pondside-Waterfoul")
Graph.add_edge("Pondside-Waterfoul", "Pondside-Feather")
# Add edges to graph
Graph.add_edge("Pondside-Feather", "Pondside-Beak")
Graph.add_edge("Pondside-Beak", "Pondside-Feather")

Graph.add_edge("Migration-Beak", "Pondside-Beak")
Graph.add_edge("Pondside-Beak", "Migration-Beak")

Graph.add_edge("Migration-Mallard", "Pondside-Mallard")
Graph.add_edge("Pondside-Mallard", "Migration-Mallard")

Graph.add_edge("Pondside-Beak", "Pondside-Mallard")
Graph.add_edge("Pondside-Mallard", "Pondside-Beak")

Graph.add_edge("Dabbler-Beak", "Pondside-Beak")
Graph.add_edge("Pondside-Beak", "Dabbler-Beak")

Graph.add_edge("Pondside-Mallard", "Dabbler-Mallard")
Graph.add_edge("Dabbler-Mallard", "Pondside-Mallard")

Graph.add_edge("Dabbler-Mallard", "Dabbler-Beak")

Graph.add_edge("Drake-Mallard", "Dabbler-Mallard")
Graph.add_edge("Dabbler-Mallard", "Duckling-Mallard")

Graph.add_edge("Drake-Beak", "Drake-Mallard")
Graph.add_edge("Duckling-Mallard", "Duckling-Beak")

Graph.add_edge("Dabbler-Beak", "Drake-Beak")
Graph.add_edge("Drake-Beak", "Dabbler-Beak")

Graph.add_edge("Drake-Beak", "Tail-Beak")
Graph.add_edge("Tail-Beak", "Drake-Beak")

Graph.add_edge("Tail-Beak", "Duckling-Beak")
Graph.add_edge("Duckling-Beak", "Tail-Beak")

Graph.add_edge("Tail-Beak", "Tail-Circle")
Graph.add_edge("Tail-Circle", "Tail-Beak")

Graph.add_edge("Tail-Circle", "Breadcrumb-Circle")

Graph.add_edge("Breadcrumb-Circle", "Breadcrumb-Waddle")
Graph.add_edge("Breadcrumb-Waddle", "Breadcrumb-Circle")

Graph.add_edge("Pondside-Waterfoul", "Circle-Waterfoul")
Graph.add_edge("Breadcrumb-Circle", "Circle-Waterfoul")
Graph.add_edge("Circle-Waterfoul", "Circle-Feather")

Graph.add_edge("Pondside-Feather", "Circle-Feather")
Graph.add_edge("Circle-Feather", "Pondside-Feather")

Graph.add_edge("Circle-Feather", "Dabbler-Circle")
Graph.add_edge("Dabbler-Beak", "Dabbler-Circle")
Graph.add_edge("Dabbler-Circle", "Tail-Circle")

def closestNode(x, y):
    closestNode = "NULL"
    minDistance = float("inf")

    for node, (xNode, yNode) in nodeMap.items():
        currentDistance = math.sqrt(pow((xNode - x),2) + pow((yNode - y), 2))

        if currentDistance <= minDistance:
            minDistance = currentDistance
            closestNode = node

    return closestNode

print(closestNode(0, 474))