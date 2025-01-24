import os
import pathlib
from typing import Union, List, Tuple
from tqdm import tqdm

from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


#########
# Tests #
#########
class MeshBuilderTests:
    def __init__(self, mesh_dir: str, mesh_scale: Union[int, float], mesh_apply_scale: float):
        self.gg = GraphGenerator()
        self.mb = MeshBuilder(mesh_dir=mesh_dir, mesh_scale=mesh_scale, mesh_apply_scale=mesh_apply_scale)

    def build_test_mesh(self, positions: List[Tuple[int, int, int]], active_connection_lists: List[List[str]],
                        output_filepath: str):
        # Build nodes_data
        nodes_data = {}
        num_of_nodes = len(positions)
        for i in range(num_of_nodes):
            nodes_data[i] = {
                "position": positions[i],
                "active_connection_list": active_connection_lists[i],
                "invalid_connection_list": list(set(self.gg.connection_types) - set(active_connection_lists[i]))
            }

        # Generate the graph
        graph = self.gg.generate_graph_3d(nodes_data=nodes_data)

        # Build the mesh
        self.mb.build_mesh(graph=graph, output_filepath=output_filepath)

    # Test Cap
    class test_cap_x1:
        positions = [(0, 0, 0), (1, 0, 0)]
        active_connection_lists = [["x"], ["x", "-x"]]

    class test_cap_x2:
        positions = [(0, 0, 0), (-1, 0, 0)]
        active_connection_lists = [["-x"], ["x", "-x"]]

    class test_cap_y1:
        positions = [(0, 0, 0), (0, 1, 0)]
        active_connection_lists = [["y"], ["y", "-y"]]

    class test_cap_y2:
        positions = [(0, 0, 0), (0, -1, 0)]
        active_connection_lists = [["-y"], ["y", "-y"]]

    class test_cap_z1:
        positions = [(0, 0, 0), (0, 0, 1)]
        active_connection_lists = [["z"], ["z", "-z"]]

    class test_cap_z2:
        positions = [(0, 0, 0), (0, 0, -1)]
        active_connection_lists = [["-z"], ["z", "-z"]]

    # Test Coupler
    class test_coupler_xx:
        positions = [(0, 0, 0), (1, 0, 0)]
        active_connection_lists = [["x", "-x"], ["x", "-x"]]

    class test_coupler_yy:
        positions = [(0, 0, 0), (0, 1, 0)]
        active_connection_lists = [["y", "-y"], ["y", "-y"]]

    class test_coupler_zz:
        positions = [(0, 0, 0), (0, 0, 1)]
        active_connection_lists = [["z", "-z"], ["z", "-z"]]

    # Test Elbow
    class test_elbow_xy1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        active_connection_lists = [["x", "y"], ["x", "-x"], ["y", "-y"]]

    class test_elbow_xy2:
        positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0)]
        active_connection_lists = [["x", "-y"], ["x", "-x"], ["y", "-y"]]

    class test_elbow_xy3:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0)]
        active_connection_lists = [["-x", "y"], ["x", "-x"], ["y", "-y"]]

    class test_elbow_xy4:
        positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0)]
        active_connection_lists = [["-x", "-y"], ["x", "-x"], ["y", "-y"]]

    class test_elbow_xz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
        active_connection_lists = [["x", "z"], ["x", "-x"], ["z", "-z"]]

    class test_elbow_xz2:
        positions = [(0, 0, 0), (1, 0, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-z"], ["x", "-x"], ["z", "-z"]]

    class test_elbow_xz3:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 0, 1)]
        active_connection_lists = [["-x", "z"], ["x", "-x"], ["z", "-z"]]

    class test_elbow_xz4:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 0, -1)]
        active_connection_lists = [["-x", "-z"], ["x", "-x"], ["z", "-z"]]

    class test_elbow_yz1:
        positions = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
        active_connection_lists = [["y", "z"], ["y", "-y"], ["z", "-z"]]

    class test_elbow_yz2:
        positions = [(0, 0, 0), (0, 1, 0), (0, 0, -1)]
        active_connection_lists = [["y", "-z"], ["y", "-y"], ["z", "-z"]]

    class test_elbow_yz3:
        positions = [(0, 0, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["-y", "z"], ["y", "-y"], ["z", "-z"]]

    class test_elbow_yz4:
        positions = [(0, 0, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["-y", "-z"], ["y", "-y"], ["z", "-z"]]

    # Test Tee
    class test_tee_xxy1:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0)]
        active_connection_lists = [["x", "-x", "y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]

    class test_tee_xxy2:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0)]
        active_connection_lists = [["x", "-x", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"]]

    class test_tee_xxz1:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1)]
        active_connection_lists = [["x", "-x", "z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]

    class test_tee_xxz2:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"]]

    class test_tee_xyy1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0)]
        active_connection_lists = [["x", "y", "-y"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]

    class test_tee_xyy2:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
        active_connection_lists = [["-x", "y", "-y"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]

    class test_tee_yyz1:
        positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["y", "-y", "z"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_tee_yyz2:
        positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["y", "-y", "-z"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_tee_xzz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "z", "-z"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]

    class test_tee_xzz2:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["-x", "z", "-z"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]

    class test_tee_yzz1:
        positions = [(0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["y", "z", "-z"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_tee_yzz2:
        positions = [(0, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["-y", "z", "-z"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    # Test ThreeWayElbow
    class test_three_way_elbow_xyz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz2:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz3:
        positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "-y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz4:
        positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz5:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1)]
        active_connection_lists = [["-x", "y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz6:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, -1)]
        active_connection_lists = [["-x", "y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz7:
        positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["-x", "-y", "z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_three_way_elbow_xyz8:
        positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["-x", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    # Test Cross
    class test_cross_xxyy:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
        active_connection_lists = [["x", "-x", "y", "-y"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"]]

    class test_cross_xxzz:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "z", "-z"], ["x", "-x"], ["x", "-x"], ["z", "-z"], ["z", "-z"]]

    class test_cross_yyzz:
        positions = [(0, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["y", "-y", "z", "-z"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    # Test FourWayTee
    class test_four_way_tee_xxyz1:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "-x", "y", "z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xxyz2:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "y", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xxyz3:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "-x", "-y", "z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xxyz4:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "-y", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xyyz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "y", "-y", "z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xyyz2:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "y", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xyyz3:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["-x", "y", "-y", "z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xyyz4:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["-x", "y", "-y", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_four_way_tee_xyzz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_four_way_tee_xyzz2:
        positions = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_four_way_tee_xyzz3:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["-x", "y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_four_way_tee_xyzz4:
        positions = [(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["-x", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    # Test FiveWayTee
    class test_five_way_tee_xxyyz1:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)]
        active_connection_lists = [["x", "-x", "y", "-y", "z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_five_way_tee_xxyyz2:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "y", "-y", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"]]

    class test_five_way_tee_xxyzz1:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "y", "z", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_five_way_tee_xxyzz2:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "-y", "z", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_five_way_tee_xyyzz1:
        positions = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "y", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    class test_five_way_tee_xyyzz2:
        positions = [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["-x", "y", "-y", "z", "-z"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    # Test Hexagonal
    class test_hexagonal:
        positions = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        active_connection_lists = [["x", "-x", "y", "-y", "z", "-z"], ["x", "-x"], ["x", "-x"], ["y", "-y"], ["y", "-y"], ["z", "-z"], ["z", "-z"]]

    # Test Custom
    class test_custom:
        positions = [(2, 0, 0), (1, 0, 0), (2, 1, 0)]
        active_connection_lists = [['-x', 'y'], ['-x', 'x'], ['-y', 'z', '-z']]

    def tests(self):
        tests_path = os.path.join(pathlib.Path(__file__).parent, "tests")
        os.makedirs(name=tests_path, exist_ok=True)

        test_list = [
            # Cap
            {"name": "cap_x1", "class": self.test_cap_x1},
            {"name": "cap_x2", "class": self.test_cap_x2},
            {"name": "cap_y1", "class": self.test_cap_y1},
            {"name": "cap_y2", "class": self.test_cap_y2},
            {"name": "cap_z1", "class": self.test_cap_z1},
            {"name": "cap_z2", "class": self.test_cap_z2},
            # Coupler
            {"name": "coupler_xx", "class": self.test_coupler_xx},
            {"name": "coupler_yy", "class": self.test_coupler_yy},
            {"name": "coupler_zz", "class": self.test_coupler_zz},
            # Elbow
            {"name": "elbow_xy1", "class": self.test_elbow_xy1},
            {"name": "elbow_xy2", "class": self.test_elbow_xy2},
            {"name": "elbow_xy3", "class": self.test_elbow_xy3},
            {"name": "elbow_xy4", "class": self.test_elbow_xy4},
            {"name": "elbow_xz1", "class": self.test_elbow_xz1},
            {"name": "elbow_xz2", "class": self.test_elbow_xz2},
            {"name": "elbow_xz3", "class": self.test_elbow_xz3},
            {"name": "elbow_xz4", "class": self.test_elbow_xz4},
            {"name": "elbow_yz1", "class": self.test_elbow_yz1},
            {"name": "elbow_yz2", "class": self.test_elbow_yz2},
            {"name": "elbow_yz3", "class": self.test_elbow_yz3},
            {"name": "elbow_yz4", "class": self.test_elbow_yz4},
            # Tee
            {"name": "tee_xxy1", "class": self.test_tee_xxy1},
            {"name": "tee_xxy2", "class": self.test_tee_xxy2},
            {"name": "tee_xxz1", "class": self.test_tee_xxz1},
            {"name": "tee_xxz2", "class": self.test_tee_xxz2},
            {"name": "tee_xyy1", "class": self.test_tee_xyy1},
            {"name": "tee_xyy2", "class": self.test_tee_xyy2},
            {"name": "tee_yyz1", "class": self.test_tee_yyz1},
            {"name": "tee_yyz2", "class": self.test_tee_yyz2},
            {"name": "tee_xzz1", "class": self.test_tee_xzz1},
            {"name": "tee_xzz2", "class": self.test_tee_xzz2},
            {"name": "tee_yzz1", "class": self.test_tee_yzz1},
            {"name": "tee_yzz2", "class": self.test_tee_yzz2},
            # ThreeWayElbow
            {"name": "three_way_elbow_xyz1", "class": self.test_three_way_elbow_xyz1},
            {"name": "three_way_elbow_xyz2", "class": self.test_three_way_elbow_xyz2},
            {"name": "three_way_elbow_xyz3", "class": self.test_three_way_elbow_xyz3},
            {"name": "three_way_elbow_xyz4", "class": self.test_three_way_elbow_xyz4},
            {"name": "three_way_elbow_xyz5", "class": self.test_three_way_elbow_xyz5},
            {"name": "three_way_elbow_xyz6", "class": self.test_three_way_elbow_xyz6},
            {"name": "three_way_elbow_xyz7", "class": self.test_three_way_elbow_xyz7},
            {"name": "three_way_elbow_xyz8", "class": self.test_three_way_elbow_xyz8},
            # Cross
            {"name": "cross_xxyy", "class": self.test_cross_xxyy},
            {"name": "cross_xxzz", "class": self.test_cross_xxzz},
            {"name": "cross_yyzz", "class": self.test_cross_yyzz},
            # FourWayTee
            {"name": "four_way_tee_xxyz1", "class": self.test_four_way_tee_xxyz1},
            {"name": "four_way_tee_xxyz2", "class": self.test_four_way_tee_xxyz2},
            {"name": "four_way_tee_xxyz3", "class": self.test_four_way_tee_xxyz3},
            {"name": "four_way_tee_xxyz4", "class": self.test_four_way_tee_xxyz4},
            {"name": "four_way_tee_xyyz1", "class": self.test_four_way_tee_xyyz1},
            {"name": "four_way_tee_xyyz2", "class": self.test_four_way_tee_xyyz2},
            {"name": "four_way_tee_xyyz3", "class": self.test_four_way_tee_xyyz3},
            {"name": "four_way_tee_xyyz4", "class": self.test_four_way_tee_xyyz4},
            {"name": "four_way_tee_xyzz1", "class": self.test_four_way_tee_xyzz1},
            {"name": "four_way_tee_xyzz2", "class": self.test_four_way_tee_xyzz2},
            {"name": "four_way_tee_xyzz3", "class": self.test_four_way_tee_xyzz3},
            {"name": "four_way_tee_xyzz4", "class": self.test_four_way_tee_xyzz4},
            # FiveWayTee
            {"name": "five_way_tee_xxyyz1", "class": self.test_five_way_tee_xxyyz1},
            {"name": "five_way_tee_xxyyz2", "class": self.test_five_way_tee_xxyyz2},
            {"name": "five_way_tee_xxyzz1", "class": self.test_five_way_tee_xxyzz1},
            {"name": "five_way_tee_xxyzz2", "class": self.test_five_way_tee_xxyzz2},
            {"name": "five_way_tee_xyyzz1", "class": self.test_five_way_tee_xyyzz1},
            {"name": "five_way_tee_xyyzz2", "class": self.test_five_way_tee_xyyzz2},
            # Hexagonal
            {"name": "hexagonal", "class": self.test_hexagonal},
            # Custom
            {"name": "custom", "class": self.test_custom}
        ]

        for test in tqdm(test_list):
            output_filepath = os.path.join(tests_path, f"{test['name']}.obj")
            test_data = test["class"]()
            self.build_test_mesh(
                positions=test_data.positions,
                active_connection_lists=test_data.active_connection_lists,
                output_filepath=output_filepath
            )


def main():
    # Mesh Parameters
    mesh_dir = "connection_types"
    mesh_scale = 66
    mesh_apply_scale = 1.0

    mbt = MeshBuilderTests(mesh_dir=mesh_dir, mesh_scale=mesh_scale, mesh_apply_scale=mesh_apply_scale)
    mbt.tests()


if __name__ == '__main__':
    main()
