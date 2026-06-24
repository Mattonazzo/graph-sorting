class Graph:
    def __init__ (self):
        self.adj_lists = {}

    def add_vertex (self, key):
        self.adj_lists [key] = {}

    def add_edge (self, from_, to, weight = 1):
        self.adj_lists [from_][to] = weight

    def vertices (self):
        return list(self.adj_lists.keys())

    def neighbors (self, key):
        return self.adj_lists[key].keys()

    def weight (self, v_from, v_to):
        return self.adj_lists[v_from].get(v_to, 0)
