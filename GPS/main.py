import json
from urllib import request
import time
import math
import networkx as nx

def get_turn_direction(prev, current, next):
    # Convert node names to coordinates
    a = nodeMap[prev]
    b = nodeMap[current]
    c = nodeMap[next]

    # Vector from prev -> current
    v1 = (b[0] - a[0], b[1] - a[1])
    # Vector from current -> next
    v2 = (c[0] - b[0], c[1] - b[1])

    # Calculate the angle using the cross product and dot product
    cross = v1[0]*v2[1] - v1[1]*v2[0]
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    angle = math.atan2(cross, dot) * (180 / math.pi)

    # Normalize the angle
    if angle > 180:
        angle -= 360
    if angle < -180:
        angle += 360

    # Determine direction
    if angle > 30:
        return "turn_left"
    elif angle < -30:
        return "turn_right"
    else:
        return "go"
def generate_directions(path):
    directions = []
    directions.append(f"go")
    for i in range(1, len(path)-1):
        prev = path[i-1]
        current = path[i]
        next = path[i+1]
        direction = get_turn_direction(prev, current, next)
        directions.append(f"{direction}")

    return directions


def closestNode(x, y):
    closestNode = "NULL"
    minDistance = float("inf")

    for node, (xNode, yNode) in nodeMap.items():
        currentDistance = math.sqrt(pow((xNode - x),2) + pow((yNode - y), 2))

        if currentDistance <= minDistance:
            minDistance = currentDistance
            closestNode = node

    return closestNode


def hypotenuse(position1, position2):

    return math.sqrt(pow(position1[0] - position2[0],2) + pow(position1[1] - position2[1], 2))

nodeMap = {"Aquatic-Beak" : [452, 29], "Aquatic-Feather" : [305, 29], "Aquatic-Waddle" : [129, 29], "Aquatic-Waterfoul" : [213, 29],
           "Breadcrumb-Circle" : [284, 393], "Breadcrumb-Waddle": [181, 459], "Circle-Feather" : [305, 296], "Circle-Waterfoul" : [273, 307],
           "Dabbler-Beak" : [452, 293], "Dabbler-Circle" : [350, 324], "Dabbler-Mallard" : [585, 293],
           "Drake-Beak" : [452, 402], "Drake-Mallard" : [576, 354], "Duckling-Beak" : [452, 474], "Duckling-Mallard" : [593, 354],
           "Migration-Beak" : [452, 135], "Migration-Feather" : [305, 135], "Migration-Mallard" : [585, 135],
           "Migration-Quack" : [29, 135], "Migration-Waddle" : [129, 135], "Migration-Waterfoul" : [213, 135],
           "Pondside-Beak" : [452, 233], "Pondside-Feather" : [305, 233], "Pondside-Mallard" : [585, 233],
           "Pondside-Quack" : [28, 329], "Pondside-Waterfoul" : [214, 241], "Pondside-Waddle" : [157, 266],
           "Tail-Beak" : [452, 465], "Tail-Circle" : [335, 387]}

edgeMap = [
    ("Pondside-Waddle", "Pondside-Quack",),
    ("Pondside-Quack", "Pondside-Waddle"),
    ("Pondside-Quack", "Breadcrumb-Waddle"),
    ("Breadcrumb-Waddle", "Pondside-Quack"),
    ("Migration-Waddle", "Migration-Quack"),
    ("Migration-Quack", "Migration-Waddle"),
    ("Migration-Quack", "Pondside-Quack"),
    ("Pondside-Quack", "Migration-Quack"),
    ("Migration-Waddle", "Migration-Waterfoul"),
    ("Migration-Waterfoul", "Migration-Waddle"),
    ("Migration-Quack", "Aquatic-Waddle"),
    ("Aquatic-Waddle", "Migration-Quack"),
    ("Migration-Waddle", "Aquatic-Waddle"),
    ("Aquatic-Waterfoul", "Aquatic-Waddle"),
    ("Aquatic-Waddle", "Aquatic-Waterfoul"),
    ("Aquatic-Waterfoul", "Aquatic-Feather"),
    ("Aquatic-Feather", "Aquatic-Waterfoul"),
    ("Aquatic-Waterfoul", "Migration-Waterfoul"),
    ("Pondside-Waddle", "Migration-Waddle"),
    ("Breadcrumb-Waddle", "Pondside-Waddle"),
    ("Migration-Waterfoul", "Pondside-Waterfoul"),
    ("Pondside-Waterfoul", "Pondside-Waddle"),
    ("Pondside-Waddle", "Pondside-Waterfoul"),
    ("Aquatic-Feather", "Aquatic-Beak"),
    ("Aquatic-Beak", "Aquatic-Feather"),
    ("Migration-Mallard", "Aquatic-Beak"),
    ("Aquatic-Beak", "Migration-Mallard"),
    ("Migration-Mallard", "Migration-Beak"),
    ("Migration-Beak", "Migration-Mallard"),
    ("Aquatic-Beak", "Migration-Beak", ),
    ("Migration-Beak", "Aquatic-Beak"),
    ("Migration-Feather", "Migration-Beak"),
    ("Migration-Beak", "Migration-Feather"),
    ("Migration-Feather", "Migration-Waterfoul"),
    ("Migration-Waterfoul", "Migration-Feather"),
    ("Aquatic-Feather", "Migration-Feather"),
    ("Migration-Feather", "Aquatic-Feather"),
    ("Migration-Feather", "Pondside-Feather"),
    ("Pondside-Feather", "Migration-Feather"),
    ("Pondside-Feather", "Pondside-Waterfoul"),
    ("Pondside-Waterfoul", "Pondside-Feather"),
    ("Pondside-Feather", "Pondside-Beak"),
    ("Pondside-Beak", "Pondside-Feather"),
    ("Migration-Beak", "Pondside-Beak"),
    ("Pondside-Beak", "Migration-Beak"),
    ("Migration-Mallard", "Pondside-Mallard"),
    ("Pondside-Mallard", "Migration-Mallard"),
    ("Pondside-Beak", "Pondside-Mallard"),
    ("Pondside-Mallard", "Pondside-Beak"),
    ("Dabbler-Beak", "Pondside-Beak"),
    ("Pondside-Beak", "Dabbler-Beak"),
    ("Pondside-Mallard", "Dabbler-Mallard"),
    ("Dabbler-Mallard", "Pondside-Mallard"),
    ("Dabbler-Mallard", "Dabbler-Beak"),
    ("Drake-Mallard", "Dabbler-Mallard"),
    ("Dabbler-Mallard", "Duckling-Mallard"),
    ("Drake-Beak", "Drake-Mallard"),
    ("Duckling-Mallard", "Duckling-Beak"),
    ("Dabbler-Beak", "Drake-Beak"),
    ("Drake-Beak", "Dabbler-Beak"),
    ("Drake-Beak", "Tail-Beak"),
    ("Tail-Beak", "Drake-Beak"),
    ("Tail-Beak", "Duckling-Beak"),
    ("Duckling-Beak", "Tail-Beak"),
    ("Tail-Beak", "Tail-Circle"),
    ("Tail-Circle", "Tail-Beak"),
    ("Tail-Circle", "Breadcrumb-Circle"),
    ("Breadcrumb-Circle", "Breadcrumb-Waddle"),
    ("Breadcrumb-Waddle", "Breadcrumb-Circle"),
    ("Pondside-Waterfoul", "Circle-Waterfoul"),
    ("Breadcrumb-Circle", "Circle-Waterfoul"),
    ("Circle-Waterfoul", "Circle-Feather"),
    ("Pondside-Feather", "Circle-Feather"),
    ("Circle-Feather", "Pondside-Feather"),
    ("Circle-Feather", "Dabbler-Circle"),
    ("Dabbler-Beak", "Dabbler-Circle"),
    ("Dabbler-Circle", "Tail-Circle")
]

# Make graph
Graph = nx.DiGraph()

# Add nodes to graph
for node, position in nodeMap.items():
    Graph.add_node(node, pos = position)

for edge in edgeMap:
    node1, node2 = edge
    position1 = nodeMap[node1]
    position2 = nodeMap[node2]

    distance = hypotenuse(position1, position2)
    Graph.add_edge(node1, node2, weight = distance)

server_ip = "10.218.79.24"
server = f"http://{server_ip}:5000"
authKey = "13"
team = 13
x = 0
y = 0
destXCoord = 0
destYCoord = 0

match = request.urlopen(server + "/match?auth=13")
if match.status == 200:
    match = json.loads(match.read())
    time.sleep(1)

    res = request.urlopen(server + "/whereami/13")
    if res.status == 200:
        res = json.loads(res.read())
        xCoord = res["position"]["x"]
        yCoord = res["position"]["y"]

        while (match["inMatch"] and match["timeRemain"] > 0):
            time.sleep(1)
            match = request.urlopen(server + "/match?auth=13")
            match = json.loads(match.read())

            fares = request.urlopen(server + "/fares")
            if fares.status == 200:
                fares = json.loads(fares.read())
                minDist = float('inf')
                id = 0
                minPath = 0
                for fare in fares:
                    srcXCoord = fare["src"]["x"]
                    srcYCoord = fare["src"]["y"]
                    destYCoord = fare["dest"]["y"]
                    destXCoord = fare["dest"]["x"]
                    path = nx.dijkstra_path(Graph, source=closestNode(xCoord, yCoord), target=closestNode(srcXCoord, srcYCoord), weight='weight')
                    distance = nx.dijkstra_path_length(Graph, source=closestNode(xCoord, yCoord), target=closestNode(srcXCoord, srcYCoord),
                                                   weight='weight')


                    if distance < minDist:
                        minDist = distance
                        id = fare["id"]
                        minPath = path
                directions = generate_directions(path)
                directions.append("x")



                path = nx.dijkstra_path(Graph, source=closestNode(srcXCoord, srcYCoord),
                                        target=closestNode(destXCoord, destYCoord), weight='weight')
                otherDirections = generate_directions(path)

                directions.extend(otherDirections)
                with open('instructions.txt', 'w') as file:
                    # Use the print function to write to the file

                    print(directions, file=file)

                res = request.urlopen(server + "/fares/claim/" + str(id) + "?auth=13")
                res = json.loads(res.read())
                if(res["success"]):
                    res = request.urlopen(server + "/whereami/13")
                    res = json.loads(res.read())
                    xCoord = res["position"]["x"]
                    yCoord = res["position"]["y"]
                    while(xCoord!=srcXCoord and yCoord != srcYCoord):
                        res = request.urlopen(server + "/whereami/13")
                        res = json.loads(res.read())
                        xCoord = res["position"]["x"]
                        yCoord = res["position"]["y"]

                time.sleep(5)

                while(xCoord!=destXCoord and yCoord != destYCoord):
                    time.sleep(1)
                    res = request.urlopen(server + "/whereami/13")
                    res = json.loads(res.read())
                    xCoord = res["position"]["x"]
                    yCoord = res["position"]["y"]

                time.sleep(5)

else:
    # Report HTTP request error
    print("Got status", str(match.status), "requesting fares")



