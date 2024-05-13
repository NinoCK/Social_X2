class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        id (any): The unique identifier of the vertex.
        edges (dict): A dictionary of edges connected to the vertex.
        data (any): Optional data associated with the vertex.
        distance (float): The distance of the vertex from a source vertex (used in graph algorithms).
        parent (Vertex): The parent vertex in a path (used in graph algorithms).
    """

    def __init__(self, id, data=None):
        self.id = id
        self.edges = {}
        self.data = data
        self.distance = float('inf')
        self.parent = None

    def add_edge(self, idb, edge):
        """
        Adds an edge to the vertex.

        Args:
            idb (any): The identifier of the vertex to connect the edge to.
            edge (Edge): The edge object to add.

        Returns:
            None
        """
        self.edges[idb] = edge

    def init_bfs(self):
        """
        Initializes the vertex for breadth-first search (BFS).

        Sets the distance to infinity and the parent to None.

        Returns:
            None
        """
        self.distance = float('inf')
        self.parent = None