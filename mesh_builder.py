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

    def apply_translation(self, mesh: trimesh.Trimesh, position: tuple):
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)

    def coupler_or_elbow(self, position: tuple, connections: list):
        if connections[0].strip("-") == connections[1].strip("-"):
            mesh = self.pipe_meshes[ConnectionTypes.Coupler].copy()

            # Rotation (In the origin)
            if {"x", "-x"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))
            if {"y", "-y"}.issubset(connections):
                pass
            if {"z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))

            # Translation
            self.apply_translation(mesh=mesh, position=position)
            return mesh
        else:
            mesh = self.pipe_meshes[ConnectionTypes.Elbow].copy()
            self.apply_translation(mesh=mesh, position=position)
            return mesh

    def tee(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Tee].copy()
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def cross(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Cross].copy()
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def five_way_cross(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.FiveWayCross].copy()
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def hexagonal_fitting(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.HexagonalFitting].copy()
        self.apply_translation(mesh=mesh, position=position)
        # No need to rotate the hexagonal fitting
        return mesh

    def build_mesh(self, G: nx.Graph, output_path = "combined_mesh.obj"):
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
        combined_mesh.export(output_path)


#########
# Tests #
#########
def build_test_mesh(gg, positions, all_active_connections, output_path):
    # Build nodes_data and position_to_node_map
    nodes_data = {}
    position_to_node_map = {}
    num_of_nodes = len(positions)
    for i in range(num_of_nodes):
        nodes_data[i] = {
            "position": positions[i],
            "active_connections": all_active_connections[i],
            "invalid_connections": list(set(gg.connection_types) - set(all_active_connections[i]))
        }
        position_to_node_map[i] = positions[i]

    # Generate the graph
    G = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)

    # Build the mesh
    mb = MeshBuilder()
    mb.build_mesh(G=G, output_path=output_path)


# Test Coupler
def test_coupler_xx(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0)]
    all_active_connections = [["x", "-x"], ["x", "-x"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)


def test_coupler_yy(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    all_active_connections = [["y", "-y"], ["y", "-y"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)


def test_coupler_zz(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    all_active_connections = [["z", "-z"], ["z", "-z"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)


# Test Elbow
def test_elbow_xy1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
    all_active_connections = [["x", "-x"], ["x", "y"], ["y", "-y"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)

def test_elbow_xy2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (1, -1, 0)]
    all_active_connections = [["x", "-x"], ["x", "-y"], ["y", "-y"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)

def test_elbow_xz1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (1, 0, 1)]
    all_active_connections = [["x", "-x"], ["x", "z"], ["z", "-z"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)

def test_elbow_xz2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (1, 0, -1)]
    all_active_connections = [["x", "-x"], ["x", "-z"], ["z", "-z"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)

def test_elbow_yz1(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 1, 1)]
    all_active_connections = [["y", "-y"], ["y", "z"], ["z", "-z"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)

def test_elbow_yz2(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 1, -1)]
    all_active_connections = [["y", "-y"], ["y", "-z"], ["z", "-z"]]

    build_test_mesh(gg=gg, positions=positions, all_active_connections=all_active_connections, output_path=output_path)



def tests():
    from graph_generator import GraphGenerator

    tests_path = os.path.join(pathlib.Path(__file__).parent, "tests")
    os.makedirs(name=tests_path, exist_ok=True)

    # Build Custom Graph
    gg = GraphGenerator()

    # Test Coupler
    test_coupler_xx(gg=gg, output_path=os.path.join(tests_path, "coupler_xx.obj"))
    test_coupler_yy(gg=gg, output_path=os.path.join(tests_path, "coupler_yy.obj"))
    test_coupler_zz(gg=gg, output_path=os.path.join(tests_path, "coupler_zz.obj"))

    # Test Elbow
    test_elbow_xy1(gg=gg, output_path=os.path.join(tests_path, "elbow_xy1.obj"))
    test_elbow_xy2(gg=gg, output_path=os.path.join(tests_path, "elbow_xy2.obj"))
    test_elbow_xz1(gg=gg, output_path=os.path.join(tests_path, "elbow_xz1.obj"))
    test_elbow_xz2(gg=gg, output_path=os.path.join(tests_path, "elbow_xz2.obj"))
    test_elbow_yz1(gg=gg, output_path=os.path.join(tests_path, "elbow_yz1.obj"))
    test_elbow_yz2(gg=gg, output_path=os.path.join(tests_path, "elbow_yz2.obj"))


if __name__ == '__main__':
    tests()
