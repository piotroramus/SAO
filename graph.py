from enum import Enum

NodeState = Enum('NodeState', 'UNTOUCHED DEFENDED BURNING')


class Graph(object):
    def __init__(self):
        self.nodes_number = 0
        self.nodes = dict()
        self.starting_nodes = list()
        super(Graph, self).__init__()

    def get_edges(self):
        edges = list()
        for node_id in self.nodes:
            for neighbor in self.nodes[node_id].neighbors:
                if (neighbor.id, node_id) not in edges:
                    edges.append((node_id, neighbor.id))
        return edges

    def get_burning_nodes(self):
        bnodes = set()
        for node_id in self.nodes:
            if self.nodes[node_id].state == NodeState.BURNING:
                bnodes.add(self.nodes[node_id])
        return bnodes

    def get_nodes(self):
        return self.nodes

    def get_starting_nodes(self):
        return self.starting_nodes

    # TODO: this method should be static and return new Graph instance
    def from_file(self, input_file):
        """ Generate graph from file format:
        n m
        1 4
        1 2
        2 3
        ...

        where:
            n - number of the vertices
            m - number of edges
        second line lists starting vertices
        the following lines determine edges
        this is exactly the format generated by the generate utility
        """
        with open(input_file, 'r') as f:
            self.nodes_number, _ = map(int, f.readline().split())
            self.starting_nodes = f.readline().split()
            self.starting_nodes = [Node(s) for s in self.starting_nodes]
            for node_id in xrange(self.nodes_number):
                self.nodes[node_id] = Node(node_id)
            for line in f:
                v1, v2 = map(int, line.split())
                self.nodes[v1].add_neighbor(self.nodes[v2])
        return self.starting_nodes

    def print_graph(self):
        """ For the time being a dumb method to help with debugging """
        for node in self.nodes.values():
            print "Node {}: {}".format(node.id, node.state)

    def reset_metadata(self):
        for v in self.nodes.values():
            v.reset_metadata()


class Node(object):
    def __init__(self, node_id, value=None):
        self.id = node_id
        self.neighbors = set()
        self.value = value
        self.reset_metadata()
        super(Node, self).__init__()

    def add_neighbor(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)

    def print_node(self):
        """ Print the graph structure accessible from this node """
        print "Node {}: {}".format(self.id, self.neighbors)

    def reset_metadata(self):
        self.state = NodeState.UNTOUCHED

    def __eq__(self, other):
        return self.id == other.id
