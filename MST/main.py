# Source for reference https://www.geeksforgeeks.org/floyd-warshall-algorithm-in-python/

# Large Infinity Value
infinity = 9999999


def floydWarshall(graph, v):

    distMatrix = list(map(lambda i: list(map(lambda j: j, i)), graph))

    # Adding up vertices one by one
    for k in range(v):
        # All vertices as source
        for i in range(v):
            # All vertices as destination
            for j in range(v):

                distMatrix[i][j] = min(distMatrix[i][j], distMatrix[i][k] + distMatrix[k][j])

# Sourced From Geeks for Geeks
def printMatrix(distMatrix, v):
    for i in range(v):
        for j in range(v):
            if distMatrix[i][j] == infinity:
                print("%7s" % "infinity", end=" ")
            else:
                print("%7d\t" % (distMatrix[i][j]), end=' ')
            if j == v - 1:
                print()

# Driver's code
if __name__ == "__main__":

    # TO BE REPLACED WITH QUACKSTON
    testGraph = []

    # Function call
    floydWarshall(testGraph, 0)