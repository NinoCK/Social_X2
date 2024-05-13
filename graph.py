import heapq
from vertex import Vertex
from edge import Edge

class Graph:
    """
    A class representing a graph data structure.

    Attributes:
    - vertices: A dictionary to store the vertices of the graph.
    - directed: A boolean indicating whether the graph is directed or not.
    - path: A string representing the path of the graph.

    Methods:
    - add_vertex: Adds a vertex to the graph.
    - add_edge: Adds an edge between two vertices in the graph.
    - get_weight: Returns the weight of an edge between two vertices.
    - set_weight: Sets the weight of an edge between two vertices.
    - get_number_of_edges: Returns the number of edges connected to a vertex.
    - display_number_of_edges: Displays the number of edges connected to each vertex.
    - display_edges: Displays all the edges in the graph.
    - get_edges: Returns the edges connected to a vertex.
    - relax: Updates the distance and parent of a vertex during Dijkstra's algorithm.
    - bfs: Performs breadth-first search starting from a given vertex.
    - dijkstra: Performs Dijkstra's algorithm starting from a given vertex.
    - print_shortest_path: Prints the shortest path from a start vertex to a destination vertex.
    """
    def __init__(self) -> None:
        self.vertices = {}
        self.directed = False
        self.path = ''

    def add_vertex(self, id, data=None):
        if id in self.vertices:
            print("Vertex already in graph")
        else:
            vertex = Vertex(id, data)
            self.vertices[id] = vertex

    def add_edge(self, user_id1, user_id2, weight=1):
        if user_id1 in self.vertices and user_id2 in self.vertices:
            edge = Edge(user_id2, weight)
            self.vertices[user_id1].add_edge(user_id2, edge)
            if not self.directed:
                edge = Edge(user_id1, weight)
                self.vertices[user_id2].add_edge(user_id1, edge)

    def get_weight(self, user_id1, user_id2):
        if user_id1 in self.vertices and user_id2 in self.vertices:
            if user_id2 in self.vertices[user_id1].edges:
                return self.vertices[user_id1].edges[user_id2].weight
        return 0

    def set_weight(self, user_id1, user_id2, weight):
        if user_id1 in self.vertices and user_id2 in self.vertices:
            if user_id2 in self.vertices[user_id1].edges:
                self.vertices[user_id1].edges[user_id2].weight = weight
            if not self.directed and user_id1 in self.vertices[user_id2].edges:
                self.vertices[user_id2].edges[user_id1].weight = weight

    def get_number_of_edges(self, name):
        if name in self.vertices:
            return len(self.vertices[name].edges)
        return 0

    def display_number_of_edges(self):
        for v in self.vertices:
            print(v, end=': ')
            print(len(self.vertices[v].edges))

    def display_edges(self):
        for v in self.vertices:
            print(v, end=': ')
            print('Edges: ', end='')
            for e in self.vertices[v].edges:
                edge = self.vertices[v].edges[e]
                print('[', e, edge.weight, '] ', end='')
            print()

    def get_edges(self, id):
        if id in self.vertices:
            return self.vertices[id].edges
        return None

    def relax(self, va, vb, w):
        if vb.distance > va.distance + w:
            vb.distance = va.distance + w
            vb.parent = va

    def bfs(self, start):
        if start not in self.vertices:
            print("Starting vertex not found")
            return
        for v in self.vertices:
            self.vertices[v].init_bfs()
        queue = []
        queue.append(self.vertices[start])
        self.vertices[start].distance = 0
        visited = set()
        visited.add(start)
        while len(queue) > 0:
            vertex = queue.pop(0)
            for e in vertex.edges:
                did = vertex.edges[e].destination
                destination = self.vertices[did]
                if did not in visited:
                    destination.parent = vertex
                    destination.distance = vertex.distance + 1
                    queue.append(destination)
                    visited.add(did)

    def dijkstra(self, start):
        if start not in self.vertices:
            print(f"Vertex {start} not found in the graph.")
            return
        self.vertices[start].distance = 0
        for v in self.vertices:
            self.vertices[v].init_bfs()
        self.vertices[start].distance = 0
        Q = []
        for vertex in self.vertices:
            Q.append(self.vertices[vertex])
        Q.sort(key=lambda x: x.distance)
        while len(Q) > 0:
            u = Q.pop(0)
            for e in u.edges:
                v = self.vertices[e]
                w = u.edges[e].weight
                self.relax(u, v, w)
            Q.sort(key=lambda x: x.distance)

    def print_shortest_path(self, start, dest):
        if dest not in self.vertices:
            print(f"Vertex {dest} not found in the graph.")
            return
        start_vertex = self.vertices[start]
        dest_vertex = self.vertices[dest]
        if dest_vertex.parent is not None:
            self.print_shortest_path(start, dest_vertex.parent.id)
        elif dest != start:
            print("No path from start to dest")
            return
        print(str(dest), end=' ')

