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
    testGraph = [
        #A
        [0, 4, 5, infinity, 6, infinity, infinity, infinity, infinity, infinity, infinity,
            4, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #B
        [4, 0, 8, 6, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #C
        [5, 8, 0, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #D
        [infinity, 6, infinity, 0, 4, infinity, 3, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #E
        [6, infinity, infinity, 4, 0, 3, infinity, infinity, infinity, infinity, infinity,
            infinity, 4, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #F
        [infinity, infinity, infinity, infinity, 3, 0, 3, 3, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #G
        [infinity, infinity, infinity, 3, infinity, infinity, 0, infinity, 3, infinity, 3,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #H
        [infinity, infinity, infinity, infinity, infinity, 3, infinity, 0, infinity, 4, infinity,
            infinity, infinity, infinity, infinity, 4, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #I
        [infinity, infinity, infinity, infinity, infinity, infinity, 3, 3, 0, 7, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #J
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, 4, 7, 0, infinity,
            infinity, infinity, infinity, infinity, 6, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #K
        [infinity, infinity, infinity, infinity, infinity, infinity, 3, infinity, infinity, infinity, 0,
            5, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, 2,
            infinity],
        #L
        [4, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, 5,
            0, 5, infinity, infinity, infinity, infinity, infinity, infinity, 2, infinity, infinity,
            infinity],
        #M
        [infinity, infinity, infinity, infinity, 4, infinity, infinity, infinity, infinity, infinity, infinity,
            5, 0, 4, infinity, infinity, infinity, 2, infinity, infinity, infinity, infinity,
            infinity],
        #N
        [infinity, infinity, infinity, infinity, infinity, 4, infinity, infinity, infinity, infinity, infinity,
            infinity, 4, 0, 2, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #O
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, 2, 0, 4, 6, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #P
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, 6, infinity,
            infinity, infinity, infinity, 4, 0, 9, infinity, infinity, infinity, infinity, infinity,
            infinity],
        #Q
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, 9, 0, 4, infinity, infinity, infinity, infinity,
            infinity],
        #R
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, 2, 3, infinity, infinity, 4, 0, 5, 4, infinity, infinity,
            infinity],
        #S
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, 5, 0, 5, 9, infinity,
            infinity],
        #T
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            2, infinity, infinity, infinity, infinity, infinity, infinity, 5, 0, infinity, 5,
            infinity],
        #U
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, 8, infinity, 0, infinity,
            1],
        #V
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, 2,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, 1, 0,
            infinity],
        #W
        [infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity, infinity,
            0]


]

    # Function call
    floydWarshall(testGraph, 0)