# Assignment 8: Graph Assignment One
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

# I used the following two videos to better understand DFS and BFS In the video they have code that I used as a base for my code. The Github link for that code follows the video.
# I had to use this because I was very confused to start with but then once I watched these videos and followed along in the code it made sense.
# https://www.youtube.com/watch?v=Urx87-NMm6c https://github.com/msambol/dsa/blob/master/search/depth_first_search.py
# https://www.youtube.com/watch?v=HZ5YTanv5QE https://github.com/msambol/dsa/blob/master/search/breadth_first_search.py

from collections import deque

# class that uses adjacency lists to represent a graph.

class Graph:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.graph = {}
        for i in range(numVertices):
            self.graph[i] = []

    # Add a connection from vertex u to vertex v
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # part 3 Depth first search and Breadth first search

    def dfs(self, target):
        visited = set()
        stack = []

        visited.add(0)
        stack.append(0)

        while stack:
            # takes the node from the top of the stack
            node = stack.pop()

            # if node that we are looking for is current node return it is found
            if node == target:
                print("DFS Found.")
                return True

            # Visit neighbors in reverse order then adds unvisited neighbors to stack to be looked at.
            for neighbor in reversed(self.graph.get(node, [])):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

        # If we exit the loop the node is not there
        print("DFS Not Found.")
        return False


    def bfs(self, target):
        visited = set()
        queue = deque([0])
        visited.add(0)

        while queue:
            # takes the node from the top of the stack
            node = queue.popleft()

            # if node that we are looking for is current node return it is found
            if node == target:
                print("BFS Found.")
                return True

            # Visit all neighbors
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # If we exit the loop the node is not there
        print("BFS Not Found.")
        return False

    # dfs and bfs print functions are used to show how the formatting of the search algorithims happen.
    # these functions are similar to the actual search algorithims they just print the vertex/node it is looking at.
    def dfsPrint(self, node):
        visited = set()
        stack = [node]
        visited.add(node)

        while stack:
            vertex = stack.pop()
            print(vertex, end=' ')

            for neighbor in reversed(self.graph[vertex]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)


    def bfsPrint(self, node):
        visited = set()
        queue = deque([node])
        visited.add(node)

        while queue:
            vertex = queue.popleft()
            print(vertex, end=' ')

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    # part 4 Topological sort

    def topologicalHelper(self, vertex, visited, stack):
        # using dfs
        visited.add(vertex)

        #recurs for the neighbors that have not been visited
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self.topologicalHelper(neighbor, visited, stack)

        # appends current vertex after looking at neighbors
        stack.append(vertex)


    def topologicalSort(self):
        visited = set()
        stack = []

        # uses the helper in order to iterate through not visited vertexes.
        for vertex in range(self.numVertices):
            if vertex not in visited:
                self.topologicalHelper(vertex, visited, stack)

        # Reverse the stack to get the correct topological ordering
        return stack[::-1]


    # part 7 Strongly connected SCCs
    # reworked the DFS to be recursive.

    def fillOrder(self, vertex, visited, stack):
        # similar to topologicalHelper but focuses on the finihing time

        visited.add(vertex)

        # Visit all unvisited neighbors
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self.fillOrder(neighbor, visited, stack)

        # Push current vertex to stack after all neighbors are visited
        stack.append(vertex)


    def dfsForSCC(self, vertex, visited, SCC):
        # Second pass of DFS for Kosarajus algorithm
        # DFS made recursive so it is easier.

        visited.add(vertex)
        SCC.append(vertex)

        # Visit all unvisited neighbors
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self.dfsForSCC(neighbor, visited, SCC)


    def findSCCS(self):
        # uses Kosarajus algorithm
        stack = []
        visited = set()

        # Step 1: do DFS to fill the stack with vertexes in order of when they finish.

        for vertex in range(self.numVertices):
            if vertex not in visited:
                self.fillOrder(vertex, visited, stack)

        # Step 2: Reverses the initial graph

        reversedGraph = Graph(self.numVertices)
        # Iterate through each vertex and reverses the edges
        for u in self.graph:
            for v in self.graph[u]:
                reversedGraph.addEdge(v, u)

        # Step 3: Do DFS again on the reversed graph
        visited.clear()
        sccList = []

        # iterates through the stack. it pops whatever is on the end of the stack and does dfs on it until it hits itself or there are no nodes it can go to.
        # once it reaches that point it makes that a SCC. then takes it off the stack
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                SCC = []
                reversedGraph.dfsForSCC(vertex, visited, SCC)
                sccList.append(SCC)

        return sccList



def main():
    # Part 1 Acyclic graph
    g = Graph(12)
    edges = [
        (0, 1), (0, 2), (1, 3),
        (2, 3), (2, 4), (3, 5),
        (4, 5), (5, 6), (6, 7), 
        (7, 8), (8, 9), (9, 10), (10, 11)
    ]
    for u, v in edges:
        g.addEdge(u, v)

    # Part 3 DFS and BFS
    print("Part 3: DFS and BFS sorting method")
    print("DFS from node 0:")
    g.dfsPrint(0)
    print("\n\nBFS from node 0:")
    g.bfsPrint(0)

    testNodes = [0, 6, -1, 12]
    print("\nPart 3: DFS and BFS Searches")
    for node in testNodes:
        print(f"\nSearch target: {node}")
        print("DFS result:")
        g.dfs(node)
        print("BFS result:")
        g.bfs(node)

    # Part 4 Topological Sort
    print("\n\nPart 4: Topological Sort")
    print(g.topologicalSort())

    # Part 7: Strongly Connected Components
    print("\n\nPart 7: Strongly Connected Components (SCCs)")
    sccGraph = Graph(12)
    sccEdges = [
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),
        (6, 7), (7, 8), (8, 6),
        (2, 3), (5, 6), (8, 9), (9, 10), (10, 11)
    ]
    for u, v in sccEdges:
        sccGraph.addEdge(u, v)

    sccList = sccGraph.findSCCS()
    print("Lists of SCCs found:")
    print(sccList)


if __name__ == "__main__":
    main()
