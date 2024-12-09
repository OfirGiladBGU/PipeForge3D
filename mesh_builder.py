from enum import Enum
import networkx as nx
import trimesh
from typing import Callable


class Connections(Enum):
    Coupler = 1
    Elbow = 2
    Tee = 3
    Cross = 4
    FiveWayCross = 5
    HexagonalFitting = 6


class MeshBuilder:
    def __init__(self):
        self.pipe_meshes = {
            "Coupler": trimesh.load(file_obj="pipes/Coupler.obj"),
            "Elbow": trimesh.load(file_obj="pipes/Elbow.obj"),
            "Tee": trimesh.load(file_obj="pipes/Tee.obj"),
            "Cross": trimesh.load(file_obj="pipes/Cross.obj"),
            "FiveWayCross": trimesh.load(file_obj="pipes/FiveWayCross.obj"),
            "HexagonalFitting": trimesh.load(file_obj="pipes/HexagonalFitting.obj")
        }
        self.connections_cases: dict[int, Callable] = {
            2: self.coupler_or_elbow,
            3: self.tee,
            4: self.cross,
            5: self.five_way_cross,
            6: self.hexagonal_fitting
        }

    def coupler_or_elbow(self, position: tuple, connections: list):
        if connections[0].strip("-") == connections[1].strip("-"):
            return self.pipe_meshes["Coupler"]
        else:
            return self.pipe_meshes["Elbow"]

    def tee(self, position: tuple, connections: list):
        return self.pipe_meshes["Tee"]

    def cross(self, position: tuple, connections: list):
        return self.pipe_meshes["Cross"]

    def five_way_cross(self, position: tuple, connections: list):
        return self.pipe_meshes["FiveWayCross"]

    def hexagonal_fitting(self, position: tuple, connections: list):
        return self.pipe_meshes["HexagonalFitting"]

    def build_mesh(self, G: nx.Graph):
        position_dict = nx.get_node_attributes(G, "position")
        connections_dict = nx.get_node_attributes(G, "connections")

        mesh_list = []
        for i in range(len(G.nodes)):
            position_i = position_dict[i]
            connections_i = connections_dict[i]
            num_of_connections = len(connections_i)

            if num_of_connections not in self.connections_cases:
                print("Invalid number of connections")
            else:
                mesh = self.connections_cases[num_of_connections](
                    position=position_i,
                    connections=connections_i
                )
                mesh_list.append(mesh)

        combined_mesh = trimesh.util.concatenate(mesh_list)
        combined_mesh.export("combined_mesh.obj")
