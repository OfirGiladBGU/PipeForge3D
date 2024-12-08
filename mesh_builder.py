from enum import Enum
import networkx as nx


class Connections(Enum):
    Coupler = 1
    Elbow = 2
    Tee = 3
    Cross = 4
    AllDirections = 5


class MeshBuilder:
    def __init__(self):
        pass

    def build_mesh(self, G: nx.Graph):
        positions = nx.get_node_attributes(G, "position")
        connections = nx.get_node_attributes(G, "connections")


