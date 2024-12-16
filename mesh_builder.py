from enum import Enum
import pathlib
import os
import networkx as nx
import numpy as np
import trimesh
from typing import Callable


class ConnectionTypes(Enum):
    Cap = "Cap.obj"
    Coupler = "Coupler.obj"
    Elbow = "Elbow.obj"
    Tee = "Tee.obj"
    ThreeWayElbow = "ThreeWayElbow.obj"
    Cross = "Cross.obj"
    FourWayTee = "FourWayTee.obj"
    FiveWayTee = "FiveWayTee.obj"
    Hexagonal = "Hexagonal.obj"


class MeshBuilder:
    def __init__(self):
        self.mesh_scale = 66
        self.pipe_meshes_path = os.path.join(pathlib.Path(__file__).parent, "pipes")
        self.pipe_meshes = {}
        for connection_type in ConnectionTypes:
            pipe_mesh_path = os.path.join(self.pipe_meshes_path, connection_type.value)
            self.pipe_meshes[connection_type] = trimesh.load(file_obj=pipe_mesh_path)

        self.connections_cases: dict[int, Callable] = {
            1: self.cap,
            2: self.coupler_or_elbow,
            3: self.tee_or_three_way_elbow,
            4: self.cross_or_four_way_tee,
            5: self.five_way_tee,
            6: self.hexagonal
        }

    def apply_translation(self, mesh: trimesh.Trimesh, position: tuple):
        position = np.array(position) * self.mesh_scale
        mesh.apply_translation(position)

    def cap(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Cap].copy()

        # Rotation (In the origin)
        if {"x"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
        if {"-x"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))

        if {"y"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
        if {"-y"}.issubset(connections):
            pass  # No need to rotate the cap

        if {"z"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
        if {"-z"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def coupler_or_elbow(self, position: tuple, connections: list):
        if connections[0].strip("-") == connections[1].strip("-"):  # Coupler
            mesh = self.pipe_meshes[ConnectionTypes.Coupler].copy()

            # Rotation (In the origin)
            if {"x", "-x"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            if {"y", "-y"}.issubset(connections):
                pass  # No need to rotate the coupler
            if {"z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
        else:  # Elbow
            mesh = self.pipe_meshes[ConnectionTypes.Elbow].copy()

            # Rotation (In the origin)
            if {"x", "y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
                pass  # No need to rotate the elbow
            if {"x", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            if {"-x", "y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            if {"-x", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
            
            if {"x", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            if {"x", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            if {"-x", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            if {"-x", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
            
            if {"y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            if {"y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
            if {"-y", "z"}.issubset(connections):
                pass  # No need to rotate the elbow
            if {"-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def tee_or_three_way_elbow(self, position: tuple, connections: list):
        stripped_connections = set([connection.strip("-") for connection in connections])
        if not {"x", "y", "z"}.issubset(stripped_connections):  # Tee
            mesh = self.pipe_meshes[ConnectionTypes.Tee].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y"}.issubset(connections):
                pass
            if {"x", "-x", "-y"}.issubset(connections):
                pass

            if {"x", "-x", "z"}.issubset(connections):
                pass
            if {"x", "-x", "-z"}.issubset(connections):
                pass

            if {"x", "y", "-y"}.issubset(connections):
                pass
            if {"-x", "y", "-y"}.issubset(connections):
                pass

            if {"y", "-y", "z"}.issubset(connections):
                pass
            if {"y", "-y", "-z"}.issubset(connections):
                pass

            if {"x", "z", "-z"}.issubset(connections):
                pass
            if {"-x", "z", "-z",}.issubset(connections):
                pass

            if {"y", "z", "-z"}.issubset(connections):
                pass
            if {"-y", "z", "-z"}.issubset(connections):
                pass

        else:  # Three-Way Elbow
            mesh = self.pipe_meshes[ConnectionTypes.ThreeWayElbow].copy()

            # Rotation (In the origin)
            if {"x", "y", "z"}.issubset(connections):
                pass
            if {"x", "y", "-z"}.issubset(connections):
                pass
            if {"x", "-y", "z"}.issubset(connections):
                pass
            if {"x", "-y", "-z"}.issubset(connections):
                pass
            if {"-x", "y", "z"}.issubset(connections):
                pass
            if {"-x", "y", "-z"}.issubset(connections):
                pass
            if {"-x", "-y", "z"}.issubset(connections):
                pass
            if {"-x", "-y", "-z"}.issubset(connections):
                pass

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def cross_or_four_way_tee(self, position: tuple, connections: list):
        stripped_connections = set([connection.strip("-") for connection in connections])
        if {"x", "y", "z"}.issubset(stripped_connections):  # Four-Way Tee
            mesh = self.pipe_meshes[ConnectionTypes.FourWayTee].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y", "z"}.issubset(connections):
                pass
            if {"x", "-x", "y", "-z"}.issubset(connections):
                pass
            if {"x", "-x", "-y", "z"}.issubset(connections):
                pass
            if {"x", "-x", "-y", "-z"}.issubset(connections):
                pass

            if {"x", "y", "-y", "z"}.issubset(connections):
                pass
            if {"x", "y", "-y", "-z"}.issubset(connections):
                pass
            if {"-x", "y", "-y", "z"}.issubset(connections):
                pass
            if {"-x", "y", "-y", "-z"}.issubset(connections):
                pass

            if {"x", "y", "z", "-z"}.issubset(connections):
                pass
            if {"x", "-y", "z", "-z"}.issubset(connections):
                pass
            if {"-x", "y", "z", "-z"}.issubset(connections):
                pass
            if {"-x", "-y", "z", "-z"}.issubset(connections):
                pass

        else: # Cross
            mesh = self.pipe_meshes[ConnectionTypes.Cross].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            if {"x", "-x", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            if {"y", "-y", "z", "-z"}.issubset(connections):
                pass  # No need to rotate the cross

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def five_way_tee(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.FiveWayTee].copy()

        # Rotation (In the origin)
        if {"x", "-x", "y", "-y", "z"}.issubset(connections):
            pass
        if {"x", "-x", "y", "-y", "-z"}.issubset(connections):
            pass

        if {"x", "-x", "y", "z", "-z"}.issubset(connections):
            pass
        if {"x", "-x", "-y", "z", "-z"}.issubset(connections):
            pass

        if {"x", "y", "-y", "z", "-z"}.issubset(connections):
            pass
        if {"-x", "y", "-y", "z", "-z"}.issubset(connections):
            pass

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def hexagonal(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Hexagonal].copy()

        # Translation (No need to rotate the hexagonal)
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def build_mesh(self, graph: nx.Graph, output_path = "combined_mesh.obj"):
        position_dict = nx.get_node_attributes(graph, "position")
        connections_dict = nx.get_node_attributes(graph, "connections")

        mesh_list = []
        for i in range(len(graph.nodes)):
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
def build_test_mesh(gg, positions: list, active_connection_lists: list, output_path: str):
    # Build nodes_data and position_to_node_map
    nodes_data = {}
    position_to_node_map = {}
    num_of_nodes = len(positions)
    for i in range(num_of_nodes):
        nodes_data[i] = {
            "position": positions[i],
            "active_connection_list": active_connection_lists[i],
            "invalid_connection_list": list(set(gg.connection_types) - set(active_connection_lists[i]))
        }
        position_to_node_map[i] = positions[i]

    # Generate the graph
    graph = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)

    # Build the mesh
    mb = MeshBuilder()
    mb.build_mesh(graph=graph, output_path=output_path)


# Test Cap
def test_cap_x1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0)]
    active_connection_lists = [["x"], ["x", "-x"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_x2(gg, output_path):
    positions = [(0, 0, 0), (-1, 0, 0)]
    active_connection_lists = [["-x"], ["x", "-x"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_y1(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    active_connection_lists = [["y"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_y2(gg, output_path):
    positions = [(0, 0, 0), (0, -1, 0)]
    active_connection_lists = [["-y"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_z1(gg, output_path):
    positions = [(0, 0, 0), (0, 0, 1)]
    active_connection_lists = [["z"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_z2(gg, output_path):
    positions = [(0, 0, 0), (0, 0, -1)]
    active_connection_lists = [["-z"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Coupler
def test_coupler_xx(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0)]
    active_connection_lists = [["x", "-x"], ["x", "-x"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_coupler_yy(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    active_connection_lists = [["y", "-y"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_coupler_zz(gg, output_path):
    positions = [(0, 0, 0), (0, 0, 1)]
    active_connection_lists = [["z", "-z"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Elbow
def test_elbow_xy1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["x", "y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy3(gg, output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["-x", "y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy4(gg, output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["-x", "-y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["x", "z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz3(gg, output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["-x", "z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz4(gg, output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "-z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz1(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
    active_connection_lists = [["y", "z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz2(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 0, -1)]
    active_connection_lists = [["y", "-z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz3(gg, output_path):
    positions = [(0, 0, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["-y", "z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz4(gg, output_path):
    positions = [(0, 0, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["-y", "-z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Tee
def test_tee_xxy1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["x", "-x", "y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxy2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-x", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxz1(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["x", "-x", "z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxz2(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xyy1(gg, output_path):
    pass


def test_tee_xyy2(gg, output_path):
    pass


def test_tee_yyz1(gg, output_path):
    pass


def test_tee_yyz2(gg, output_path):
    pass


def test_tee_xzz1(gg, output_path):
    pass


def test_tee_xzz2(gg, output_path):
    pass


def test_tee_yzz1(gg, output_path):
    pass


def test_tee_yzz2(gg, output_path):
    pass


# Test Cross
def test_cross_xxyy(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-x", "y", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cross_xxzz(gg, output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "z", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cross_yyzz(gg, output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["y", "-y", "z", "-z"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Custom Test
def custom_test(gg, output_path):
    positions = [(2, 0, 0), (1, 0, 0), (2, 1, 0)]
    active_connection_lists = [['-x', 'y'], ['-x', 'x'], ['-y', 'z', '-z']]
    build_test_mesh(gg=gg, positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def tests():
    from graph_generator import GraphGenerator

    tests_path = os.path.join(pathlib.Path(__file__).parent, "tests")
    os.makedirs(name=tests_path, exist_ok=True)

    # Build Custom Graph
    gg = GraphGenerator()

    # Test Cap
    test_cap_x1(gg=gg, output_path=os.path.join(tests_path, "cap_x1.obj"))
    test_cap_x2(gg=gg, output_path=os.path.join(tests_path, "cap_x2.obj"))

    test_cap_y1(gg=gg, output_path=os.path.join(tests_path, "cap_y1.obj"))
    test_cap_y2(gg=gg, output_path=os.path.join(tests_path, "cap_y2.obj"))

    test_cap_z1(gg=gg, output_path=os.path.join(tests_path, "cap_z1.obj"))
    test_cap_z2(gg=gg, output_path=os.path.join(tests_path, "cap_z2.obj"))

    # Test Coupler
    test_coupler_xx(gg=gg, output_path=os.path.join(tests_path, "coupler_xx.obj"))

    test_coupler_yy(gg=gg, output_path=os.path.join(tests_path, "coupler_yy.obj"))

    test_coupler_zz(gg=gg, output_path=os.path.join(tests_path, "coupler_zz.obj"))

    # Test Elbow
    test_elbow_xy1(gg=gg, output_path=os.path.join(tests_path, "elbow_xy1.obj"))
    test_elbow_xy2(gg=gg, output_path=os.path.join(tests_path, "elbow_xy2.obj"))
    test_elbow_xy3(gg=gg, output_path=os.path.join(tests_path, "elbow_xy3.obj"))
    test_elbow_xy4(gg=gg, output_path=os.path.join(tests_path, "elbow_xy4.obj"))

    test_elbow_xz1(gg=gg, output_path=os.path.join(tests_path, "elbow_xz1.obj"))
    test_elbow_xz2(gg=gg, output_path=os.path.join(tests_path, "elbow_xz2.obj"))
    test_elbow_xz3(gg=gg, output_path=os.path.join(tests_path, "elbow_xz3.obj"))
    test_elbow_xz4(gg=gg, output_path=os.path.join(tests_path, "elbow_xz4.obj"))

    test_elbow_yz1(gg=gg, output_path=os.path.join(tests_path, "elbow_yz1.obj"))
    test_elbow_yz2(gg=gg, output_path=os.path.join(tests_path, "elbow_yz2.obj"))
    test_elbow_yz3(gg=gg, output_path=os.path.join(tests_path, "elbow_yz3.obj"))
    test_elbow_yz4(gg=gg, output_path=os.path.join(tests_path, "elbow_yz4.obj"))

    # Test Tee
    test_tee_xxy1(gg=gg, output_path=os.path.join(tests_path, "tee_xxy1.obj"))
    test_tee_xxy2(gg=gg, output_path=os.path.join(tests_path, "tee_xxy2.obj"))

    test_tee_xxz1(gg=gg, output_path=os.path.join(tests_path, "tee_xxz1.obj"))
    test_tee_xxz2(gg=gg, output_path=os.path.join(tests_path, "tee_xxz2.obj"))

    test_tee_xyy1(gg=gg, output_path=os.path.join(tests_path, "tee_xyy1.obj"))
    test_tee_xyy2(gg=gg, output_path=os.path.join(tests_path, "tee_xyy2.obj"))

    test_tee_yyz1(gg=gg, output_path=os.path.join(tests_path, "tee_yyz1.obj"))
    test_tee_yyz2(gg=gg, output_path=os.path.join(tests_path, "tee_yyz2.obj"))

    test_tee_xzz1(gg=gg, output_path=os.path.join(tests_path, "tee_xzz1.obj"))
    test_tee_xzz2(gg=gg, output_path=os.path.join(tests_path, "tee_xzz2.obj"))

    test_tee_yzz1(gg=gg, output_path=os.path.join(tests_path, "tee_yzz1.obj"))
    test_tee_yzz2(gg=gg, output_path=os.path.join(tests_path, "tee_yzz2.obj"))


    # Test ThreeWayElbow

    # Test Cross
    test_cross_xxyy(gg=gg, output_path=os.path.join(tests_path, "cross_xxyy.obj"))

    test_cross_xxzz(gg=gg, output_path=os.path.join(tests_path, "cross_xxzz.obj"))

    test_cross_yyzz(gg=gg, output_path=os.path.join(tests_path, "cross_yyzz.obj"))

    # Test FourWayTee

    # Test FiveWayCross

    # Test Hexagonal

    # Custom Test
    custom_test(gg=gg, output_path=os.path.join(tests_path, "custom.obj"))


if __name__ == '__main__':
    tests()
