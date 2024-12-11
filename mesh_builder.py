from enum import Enum
import pathlib
import os
import networkx as nx
import numpy as np
import trimesh
from typing import Callable


class ConnectionTypes(Enum):
    Coupler = "Coupler.obj"
    Elbow = "Elbow.obj"
    Tee = "Tee.obj"
    Cross = "Cross.obj"
    FiveWayCross = "FiveWayCross.obj"
    HexagonalFitting = "HexagonalFitting.obj"


class MeshBuilder:
    def __init__(self):
        self.mesh_scale = 66
        self.pipe_meshes_path = os.path.join(pathlib.Path(__file__).parent, "pipes")
        self.pipe_meshes = {}
        for connection_type in ConnectionTypes:
            pipe_mesh_path = os.path.join(self.pipe_meshes_path, connection_type.value)
            self.pipe_meshes[connection_type] = trimesh.load(file_obj=pipe_mesh_path)

        self.connections_cases: dict[int, Callable] = {
            2: self.coupler_or_elbow,
            3: self.tee,
            4: self.cross,
            5: self.five_way_cross,
            6: self.hexagonal_fitting
        }

    def coupler_or_elbow(self, position: tuple, connections: list):
        if connections[0].strip("-") == connections[1].strip("-"):
            mesh = self.pipe_meshes[ConnectionTypes.Coupler].copy()
            position = np.array(position) * self.mesh_scale
            mesh.apply_translation(position)
            return mesh
        else:
            mesh = self.pipe_meshes[ConnectionTypes.Elbow].copy()
            position = np.array(position) * self.mesh_scale
            mesh.apply_translation(position)
            return mesh

    def tee(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Tee].copy()
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)
        return mesh

    def cross(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Cross].copy()
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)
        return mesh

    def five_way_cross(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.FiveWayCross].copy()
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)
        return mesh

    def hexagonal_fitting(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.HexagonalFitting].copy()
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)
        return mesh

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
