# Assignment 9: Graph Assignment Two
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

from collections import deque

class FlowGraph:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.graph = {}
        self.capacity = {}

        for i in range(numVertices):
            self.graph[i] = []
            self.capacity[i] = {}

    # Add a connection from vertex u to vertex v and capacity of the edge
    def addEdge(self, u, v, cap):
        self.graph[u].append(v)
        self.capacity[u][v] = cap

        # adds a reverse edge with capacity of 0 for the residual graph
        if u not in self.graph[v]:
            self.graph[v].append(u)
        self.capacity[v][u] = self.capacity[v].get(u, 0)

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque()
        queue.append(source)
        visited.add(source)

        while queue:
            # takes the node from the top of the stack
            current = queue.popleft()

            # Visit all neighbors
            for neighbor in self.graph[current]:
                # Only consider unvisited neighbors with available capacity
                if neighbor not in visited and self.capacity[current][neighbor] > 0:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    # if the neighbor is the sink it will return as it is a valid path.
                    if neighbor == sink:
                        return True
                    queue.append(neighbor)

        # if it reaches here there is no path found to the sink.
        return False

    def fordFulkerson(self, source, sink):
        parent = {}     # stores the path from source to sink
        maxFlow = 0

        # this loop will only run when there is a valid path from source to sink
        while self.bfs(source, sink, parent):
            # Step 1: finds the bottleneck capacity amount for the path aka the minimum capacity along the path
            pathFlow = float('inf')
            s = sink
            while s != source:
                pathFlow = min(pathFlow, self.capacity[parent[s]][s])
                s = parent[s]

            # Step 2: updates the residual graph to subract all the capacities by the bottleneck
            v = sink
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= pathFlow   # reduce flow from u to v
                v = parent[v]

            # Step 3: adds the current path flow to the max flow. then clears path for next run through
            maxFlow += pathFlow
            parent.clear()

        return maxFlow



def testGivenGraph():
    print("Given Graph")
    g = FlowGraph(6)
    g.addEdge(0, 1, 4)
    g.addEdge(0, 2, 2)
    g.addEdge(1, 2, 1)
    g.addEdge(1, 3, 2)
    g.addEdge(1, 4, 4)
    g.addEdge(2, 4, 2)
    g.addEdge(3, 5, 3)
    g.addEdge(4, 5, 3)

    maxFlow = g.fordFulkerson(0, 5)
    print(f"Maximum flow from source to sink is: {maxFlow}")


def testCustomGraph():
    print("\nCustom Graph")
    g = FlowGraph(10)
    g.addEdge(0, 1, 6)
    g.addEdge(0, 2, 10)
    g.addEdge(1, 4, 8)
    g.addEdge(2, 3, 4)
    g.addEdge(2, 5, 8)
    g.addEdge(3, 1, 11)
    g.addEdge(3, 5, 5)
    g.addEdge(3, 6, 6)
    g.addEdge(4, 6, 9)
    g.addEdge(5, 7, 8)
    g.addEdge(6, 7, 7)
    g.addEdge(6, 9, 12)
    g.addEdge(7, 9, 13)
    g.addEdge(8, 9, 20)

    maxFlow = g.fordFulkerson(0, 9)
    print(f"Maximum flow from source to sink is: {maxFlow}")


def main():
    testGivenGraph()
    testCustomGraph()


if __name__ == "__main__":
    main()
