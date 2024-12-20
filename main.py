import os
import pathlib
from typing import Union
from tqdm import tqdm

from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


def generate_output_files(num_of_nodes: int, num_of_outputs: int, graph_scale: int, pcd_percentage: float,
                          mesh_dir: str, mesh_scale: Union[int, float]):
    output_dir = os.path.join(pathlib.Path(__file__).parent, "output")
    os.makedirs(name=output_dir, exist_ok=True)

    gg = GraphGenerator()
    zfill_num = len(str(num_of_outputs))
    for i in tqdm(range(num_of_outputs)):
        num_str_format = str(i + 1).zfill(zfill_num)
        output_path = os.path.join(output_dir, num_str_format)

        # Generate the graph
        nodes_data = gg.generate_random_3d_nodes_data(num_of_nodes=num_of_nodes, output_filepath=f"{output_path}.json")
        graph = gg.generate_graph_3d(nodes_data=nodes_data)
        gg.plot_graph_3d(graph=graph, scale=graph_scale, output_filepath=f"{output_path}.png")

        # Build the mesh and point cloud
        mb = MeshBuilder(mesh_dir=mesh_dir, mesh_scale=mesh_scale)
        mesh = mb.build_mesh(graph=graph, output_filepath=f"{output_path}.obj")
        pcd = mb.build_pcd(input_object=mesh, percentage=pcd_percentage, output_filepath=f"{output_path}.pcd")


def main():
    # Generate Parameters
    num_of_nodes = 50
    num_of_outputs = 20
    graph_scale = 1
    pcd_percentage = 1.0

    # Mesh Parameters
    mesh_dir = "connection_types"
    mesh_scale = 66

    generate_output_files(
        num_of_nodes=num_of_nodes,
        num_of_outputs=num_of_outputs,
        graph_scale=graph_scale,
        pcd_percentage=pcd_percentage,
        mesh_dir=mesh_dir,
        mesh_scale=mesh_scale
    )


if __name__ == '__main__':
    main()
