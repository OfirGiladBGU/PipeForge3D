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
        elif {"-x"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))

        elif {"y"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
        elif {"-y"}.issubset(connections):
            pass  # No need to rotate the cap

        elif {"z"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
        elif {"-z"}.issubset(connections):
            mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

        else:
            raise ValueError("Invalid connections for cap")

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def coupler_or_elbow(self, position: tuple, connections: list):
        if connections[0].strip("-") == connections[1].strip("-"):  # Coupler
            mesh = self.pipe_meshes[ConnectionTypes.Coupler].copy()

            # Rotation (In the origin)
            if {"x", "-x"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"y", "-y"}.issubset(connections):
                pass  # No need to rotate the coupler
            elif {"z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            else:
                raise ValueError("Invalid connections for coupler")

        else:  # Elbow
            mesh = self.pipe_meshes[ConnectionTypes.Elbow].copy()

            # Rotation (In the origin)
            if {"x", "y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"x", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"-x", "y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            elif {"-x", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
            
            elif {"x", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"x", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"-x", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            elif {"-x", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
            
            elif {"y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
            elif {"-y", "z"}.issubset(connections):
                pass  # No need to rotate the elbow
            elif {"-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            else:
                raise ValueError("Invalid connections for elbow")

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def tee_or_three_way_elbow(self, position: tuple, connections: list):
        stripped_connections = set([connection.strip("-") for connection in connections])
        if not {"x", "y", "z"}.issubset(stripped_connections):  # Tee
            mesh = self.pipe_meshes[ConnectionTypes.Tee].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "-x", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))

            elif {"x", "-x", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"x", "-x", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))

            elif {"x", "y", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"-x", "y", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))

            elif {"y", "-y", "z"}.issubset(connections):
                pass  # No need to rotate the tee
            elif {"y", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))

            elif {"x", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
            elif {"-x", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            elif {"y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"-y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            else:
                raise ValueError("Invalid connections for tee")

        else:  # Three-Way Elbow
            mesh = self.pipe_meshes[ConnectionTypes.ThreeWayElbow].copy()

            # Rotation (In the origin)
            if {"x", "y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "-y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"-x", "y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"-x", "y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"-x", "-y", "z"}.issubset(connections):
                pass  # No need to rotate the three-way elbow
            elif {"-x", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            else:
                raise ValueError("Invalid connections for three way elbow")

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def cross_or_four_way_tee(self, position: tuple, connections: list):
        stripped_connections = set([connection.strip("-") for connection in connections])
        if not {"x", "y", "z"}.issubset(stripped_connections):  # Cross
            mesh = self.pipe_meshes[ConnectionTypes.Cross].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y", "-y"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "-x", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"y", "-y", "z", "-z"}.issubset(connections):
                pass  # No need to rotate the cross

            else:
                raise ValueError("Invalid connections for cross")

        else:  # Four-Way Tee
            mesh = self.pipe_meshes[ConnectionTypes.FourWayTee].copy()

            # Rotation (In the origin)
            if {"x", "-x", "y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            elif {"x", "-x", "y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"x", "-x", "-y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"x", "-x", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            elif {"x", "y", "-y", "z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"x", "y", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 1, 0]))
            elif {"-x", "y", "-y", "z"}.issubset(connections):
                pass  # No need to rotate the four-way tee
            elif {"-x", "y", "-y", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, -1, 0]))

            elif {"x", "y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, -1]))
            elif {"x", "-y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[0, 0, 1]))
            elif {"-x", "y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[-1, 0, 0]))
            elif {"-x", "-y", "z", "-z"}.issubset(connections):
                mesh.apply_transform(trimesh.transformations.rotation_matrix(angle=np.pi / 2, direction=[1, 0, 0]))

            else:
                raise ValueError("Invalid connections for four way tee")

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def five_way_tee(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.FiveWayTee].copy()

        # Rotation (In the origin)
        if {"x", "-x", "y", "-y", "z"}.issubset(connections):
            pass  # No need to rotate the five-way tee
        elif {"x", "-x", "y", "-y", "-z"}.issubset(connections):
            pass

        elif {"x", "-x", "y", "z", "-z"}.issubset(connections):
            pass
        elif {"x", "-x", "-y", "z", "-z"}.issubset(connections):
            pass

        elif {"x", "y", "-y", "z", "-z"}.issubset(connections):
            pass
        elif {"-x", "y", "-y", "z", "-z"}.issubset(connections):
            pass

        else:
            raise ValueError("Invalid connections for five way tee")

        # Translation
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def hexagonal(self, position: tuple, connections: list):
        mesh = self.pipe_meshes[ConnectionTypes.Hexagonal].copy()

        if not {"x", "-x", "y", "-y", "z", "-z"}.issubset(connections):
            raise ValueError("Invalid connections for hexagonal")

        # Translation (No need to rotate the hexagonal)
        self.apply_translation(mesh=mesh, position=position)
        return mesh

    def build_mesh(self, graph: nx.Graph, output_path="combined_mesh.obj"):
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


def test():
    from graph_generator import GraphGenerator

    # Parameters
    num_of_nodes = 20

    # Generate and plot the graph
    gg = GraphGenerator()
    nodes_data, position_to_node_map = gg.generate_random_3d_nodes_structure(num_of_nodes=num_of_nodes)
    graph = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)
    # print(nodes_data)
    gg.plot_graph_3d(graph=graph)

    # Build the mesh
    mb = MeshBuilder()
    mb.build_mesh(graph=graph, output_path="output.obj")


if __name__ == '__main__':
    test()
