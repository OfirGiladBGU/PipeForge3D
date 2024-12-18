import os
import pathlib

from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


#########
# Tests #
#########
def build_test_mesh(positions: list, active_connection_lists: list, output_path: str):
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
def test_cap_x1(output_path):
    positions = [(0, 0, 0), (1, 0, 0)]
    active_connection_lists = [["x"], ["x", "-x"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_x2(output_path):
    positions = [(0, 0, 0), (-1, 0, 0)]
    active_connection_lists = [["-x"], ["x", "-x"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_y1(output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    active_connection_lists = [["y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_y2(output_path):
    positions = [(0, 0, 0), (0, -1, 0)]
    active_connection_lists = [["-y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_z1(output_path):
    positions = [(0, 0, 0), (0, 0, 1)]
    active_connection_lists = [["z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cap_z2(output_path):
    positions = [(0, 0, 0), (0, 0, -1)]
    active_connection_lists = [["-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Coupler
def test_coupler_xx(output_path):
    positions = [(0, 0, 0), (1, 0, 0)]
    active_connection_lists = [["x", "-x"], ["x", "-x"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_coupler_yy(output_path):
    positions = [(0, 0, 0), (0, 1, 0)]
    active_connection_lists = [["y", "-y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_coupler_zz(output_path):
    positions = [(0, 0, 0), (0, 0, 1)]
    active_connection_lists = [["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Elbow
def test_elbow_xy1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["x", "y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy3(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["-x", "y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xy4(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["-x", "-y"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["x", "z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz3(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["-x", "z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_xz4(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "-z"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz1(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
    active_connection_lists = [["y", "z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz2(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 0, -1)]
    active_connection_lists = [["y", "-z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz3(output_path):
    positions = [(0, 0, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["-y", "z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_elbow_yz4(output_path):
    positions = [(0, 0, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["-y", "-z"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Tee
def test_tee_xxy1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0)]
    active_connection_lists = [["x", "-x", "y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxy2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-x", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1)]
    active_connection_lists = [["x", "-x", "z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xxz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xyy1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0)]
    active_connection_lists = [["x", "y", "-y"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xyy2(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
    active_connection_lists = [["-x", "y", "-y"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_yyz1(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["y", "-y", "z"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_yyz2(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["y", "-y", "-z"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xzz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "z", "-z"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_xzz2(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["-x", "z", "-z"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_yzz1(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["y", "z", "-z"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_tee_yzz2(output_path):
    positions = [(0, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["-y", "z", "-z"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test ThreeWayElbow
def test_three_way_elbow_xyz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    active_connection_lists = [["x", "y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, -1)]
    active_connection_lists = [["x", "y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz3(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["x", "-y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz4(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz5(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1)]
    active_connection_lists = [["-x", "y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz6(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz7(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["-x", "-y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_three_way_elbow_xyz8(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Cross
def test_cross_xxyy(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
    active_connection_lists = [["x", "-x", "y", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cross_xxzz(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "z", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_cross_yyzz(output_path):
    positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["y", "-y", "z", "-z"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test FourWayTee
def test_four_way_tee_xxyz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1)]
    active_connection_lists = [["x", "-x", "y", "z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xxyz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "y", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xxyz3(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["x", "-x", "-y", "z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xxyz4(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["x", "-x", "-y", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyyz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
    active_connection_lists = [["x", "y", "-y", "z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyyz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["x", "y", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyyz3(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "y", "-y", "z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyyz4(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
    active_connection_lists = [["-x", "y", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyzz1(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyzz2(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyzz3(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["-x", "y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def test_four_way_tee_xyzz4(output_path):
    positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["-x", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test FiveWayTee
def test_five_way_tee_xxyyz1(output_path):
    pass


def test_five_way_tee_xxyyz2(output_path):
    pass


def test_five_way_tee_xxyzz1(output_path):
    pass


def test_five_way_tee_xxyzz2(output_path):
    pass


def test_five_way_tee_xyyzz1(output_path):
    pass


def test_five_way_tee_xyyzz2(output_path):
    pass


# Test Hexagonal
def test_hexagonal(output_path):
    positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    active_connection_lists = [["x", "x", "y", "-y", "z", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


# Test Custom
def test_custom(output_path):
    positions = [(2, 0, 0), (1, 0, 0), (2, 1, 0)]
    active_connection_lists = [['-x', 'y'], ['-x', 'x'], ['-y', 'z', '-z']]
    build_test_mesh(positions=positions, active_connection_lists=active_connection_lists, output_path=output_path)


def tests():
    tests_path = os.path.join(pathlib.Path(__file__).parent, "tests")
    os.makedirs(name=tests_path, exist_ok=True)

    # Test Cap
    test_cap_x1(output_path=os.path.join(tests_path, "cap_x1.obj"))
    test_cap_x2(output_path=os.path.join(tests_path, "cap_x2.obj"))

    test_cap_y1(output_path=os.path.join(tests_path, "cap_y1.obj"))
    test_cap_y2(output_path=os.path.join(tests_path, "cap_y2.obj"))

    test_cap_z1(output_path=os.path.join(tests_path, "cap_z1.obj"))
    test_cap_z2(output_path=os.path.join(tests_path, "cap_z2.obj"))

    # Test Coupler
    test_coupler_xx(output_path=os.path.join(tests_path, "coupler_xx.obj"))

    test_coupler_yy(output_path=os.path.join(tests_path, "coupler_yy.obj"))

    test_coupler_zz(output_path=os.path.join(tests_path, "coupler_zz.obj"))

    # Test Elbow
    test_elbow_xy1(output_path=os.path.join(tests_path, "elbow_xy1.obj"))
    test_elbow_xy2(output_path=os.path.join(tests_path, "elbow_xy2.obj"))
    test_elbow_xy3(output_path=os.path.join(tests_path, "elbow_xy3.obj"))
    test_elbow_xy4(output_path=os.path.join(tests_path, "elbow_xy4.obj"))

    test_elbow_xz1(output_path=os.path.join(tests_path, "elbow_xz1.obj"))
    test_elbow_xz2(output_path=os.path.join(tests_path, "elbow_xz2.obj"))
    test_elbow_xz3(output_path=os.path.join(tests_path, "elbow_xz3.obj"))
    test_elbow_xz4(output_path=os.path.join(tests_path, "elbow_xz4.obj"))

    test_elbow_yz1(output_path=os.path.join(tests_path, "elbow_yz1.obj"))
    test_elbow_yz2(output_path=os.path.join(tests_path, "elbow_yz2.obj"))
    test_elbow_yz3(output_path=os.path.join(tests_path, "elbow_yz3.obj"))
    test_elbow_yz4(output_path=os.path.join(tests_path, "elbow_yz4.obj"))

    # Test Tee
    test_tee_xxy1(output_path=os.path.join(tests_path, "tee_xxy1.obj"))
    test_tee_xxy2(output_path=os.path.join(tests_path, "tee_xxy2.obj"))

    test_tee_xxz1(output_path=os.path.join(tests_path, "tee_xxz1.obj"))
    test_tee_xxz2(output_path=os.path.join(tests_path, "tee_xxz2.obj"))

    test_tee_xyy1(output_path=os.path.join(tests_path, "tee_xyy1.obj"))
    test_tee_xyy2(output_path=os.path.join(tests_path, "tee_xyy2.obj"))

    test_tee_yyz1(output_path=os.path.join(tests_path, "tee_yyz1.obj"))
    test_tee_yyz2(output_path=os.path.join(tests_path, "tee_yyz2.obj"))

    test_tee_xzz1(output_path=os.path.join(tests_path, "tee_xzz1.obj"))
    test_tee_xzz2(output_path=os.path.join(tests_path, "tee_xzz2.obj"))

    test_tee_yzz1(output_path=os.path.join(tests_path, "tee_yzz1.obj"))
    test_tee_yzz2(output_path=os.path.join(tests_path, "tee_yzz2.obj"))

    # Test ThreeWayElbow
    test_three_way_elbow_xyz1(output_path=os.path.join(tests_path, "three_way_elbow_xyz1.obj"))
    test_three_way_elbow_xyz2(output_path=os.path.join(tests_path, "three_way_elbow_xyz2.obj"))
    test_three_way_elbow_xyz3(output_path=os.path.join(tests_path, "three_way_elbow_xyz3.obj"))
    test_three_way_elbow_xyz4(output_path=os.path.join(tests_path, "three_way_elbow_xyz4.obj"))
    test_three_way_elbow_xyz5(output_path=os.path.join(tests_path, "three_way_elbow_xyz5.obj"))
    test_three_way_elbow_xyz6(output_path=os.path.join(tests_path, "three_way_elbow_xyz6.obj"))
    test_three_way_elbow_xyz7(output_path=os.path.join(tests_path, "three_way_elbow_xyz7.obj"))
    test_three_way_elbow_xyz8(output_path=os.path.join(tests_path, "three_way_elbow_xyz8.obj"))

    # Test Cross
    test_cross_xxyy(output_path=os.path.join(tests_path, "cross_xxyy.obj"))

    test_cross_xxzz(output_path=os.path.join(tests_path, "cross_xxzz.obj"))

    test_cross_yyzz(output_path=os.path.join(tests_path, "cross_yyzz.obj"))

    # Test FourWayTee
    test_four_way_tee_xxyz1(output_path=os.path.join(tests_path, "four_way_tee_xxyz1.obj"))
    test_four_way_tee_xxyz2(output_path=os.path.join(tests_path, "four_way_tee_xxyz2.obj"))
    test_four_way_tee_xxyz3(output_path=os.path.join(tests_path, "four_way_tee_xxyz3.obj"))
    test_four_way_tee_xxyz4(output_path=os.path.join(tests_path, "four_way_tee_xxyz4.obj"))

    test_four_way_tee_xyyz1(output_path=os.path.join(tests_path, "four_way_tee_xyyz1.obj"))
    test_four_way_tee_xyyz2(output_path=os.path.join(tests_path, "four_way_tee_xyyz2.obj"))
    test_four_way_tee_xyyz3(output_path=os.path.join(tests_path, "four_way_tee_xyyz3.obj"))
    test_four_way_tee_xyyz4(output_path=os.path.join(tests_path, "four_way_tee_xyyz4.obj"))

    test_four_way_tee_xyzz1(output_path=os.path.join(tests_path, "four_way_tee_xyzz1.obj"))
    test_four_way_tee_xyzz2(output_path=os.path.join(tests_path, "four_way_tee_xyzz2.obj"))
    test_four_way_tee_xyzz3(output_path=os.path.join(tests_path, "four_way_tee_xyzz3.obj"))
    test_four_way_tee_xyzz4(output_path=os.path.join(tests_path, "four_way_tee_xyzz4.obj"))

    # Test FiveWayTee
    test_five_way_tee_xxyyz1(output_path=os.path.join(tests_path, "five_way_tee_xxyyz1.obj"))
    test_five_way_tee_xxyyz2(output_path=os.path.join(tests_path, "five_way_tee_xxyyz2.obj"))

    test_five_way_tee_xxyzz1(output_path=os.path.join(tests_path, "five_way_tee_xxyzz1.obj"))
    test_five_way_tee_xxyzz2(output_path=os.path.join(tests_path, "five_way_tee_xxyzz2.obj"))

    test_five_way_tee_xyyzz1(output_path=os.path.join(tests_path, "five_way_tee_xyyzz1.obj"))
    test_five_way_tee_xyyzz2(output_path=os.path.join(tests_path, "five_way_tee_xyyzz2.obj"))

    # Test Hexagonal
    test_hexagonal(output_path=os.path.join(tests_path, "hexagonal.obj"))

    # Test Custom
    test_custom(output_path=os.path.join(tests_path, "custom.obj"))


if __name__ == '__main__':
    gg = GraphGenerator()
    tests()
