import os
import pathlib
from typing import Union
from tqdm import tqdm
import json

from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


def generate_output_files(num_of_nodes: int, num_of_outputs: int, graph_scale: int,
                          pcd_use_sample_method: bool, pcd_points_to_sample: Union[float, int],
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
        pcd = mb.build_pcd(input_object=mesh,
                           use_sample_method=pcd_use_sample_method, points_to_sample=pcd_points_to_sample,
                           output_filepath=f"{output_path}.pcd")


def build_mesh_from_json(json_filepath: str, graph_scale: int,
                          pcd_use_sample_method: bool, pcd_points_to_sample: Union[float, int],
                          mesh_dir: str, mesh_scale: Union[int, float]):
    output_dir = os.path.join(pathlib.Path(__file__).parent, "from_json_output")
    os.makedirs(name=output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, pathlib.Path(json_filepath).stem)

    with open(json_filepath, "r") as f:
        nodes_data = json.load(f)

    gg = GraphGenerator()
    graph = gg.generate_graph_3d(nodes_data=nodes_data)
    gg.plot_graph_3d(graph=graph, scale=graph_scale, output_filepath=f"{output_path}.png")

    # Build the mesh and point cloud
    mb = MeshBuilder(mesh_dir=mesh_dir, mesh_scale=mesh_scale)
    mesh = mb.build_mesh(graph=graph, output_filepath=f"{output_path}.obj")
    pcd = mb.build_pcd(input_object=mesh,
                       use_sample_method=pcd_use_sample_method, points_to_sample=pcd_points_to_sample,
                       output_filepath=f"{output_path}.pcd")


def generate_data():
    # Generate Parameters
    num_of_nodes = 50
    num_of_outputs = 20
    graph_scale = 1
    pcd_use_sample_method = False
    pcd_points_to_sample = 1.0

    # Mesh Parameters
    mesh_dir = "connection_types"
    mesh_scale = 66

    generate_output_files(
        num_of_nodes=num_of_nodes,
        num_of_outputs=num_of_outputs,
        graph_scale=graph_scale,
        pcd_use_sample_method=pcd_use_sample_method,
        pcd_points_to_sample=pcd_points_to_sample,
        mesh_dir=mesh_dir,
        mesh_scale=mesh_scale
    )

def build_data_from_json():
    # JSON Parameters
    json_filepath = "output/01.json"

    # Generate Parameters
    graph_scale = 1
    pcd_use_sample_method = False
    pcd_points_to_sample = 1.0

    # Mesh Parameters
    mesh_dir = "connection_types"
    mesh_scale = 66

    build_mesh_from_json(
        json_filepath=json_filepath,
        graph_scale=graph_scale,
        pcd_use_sample_method=pcd_use_sample_method,
        pcd_points_to_sample=pcd_points_to_sample,
        mesh_dir=mesh_dir,
        mesh_scale=mesh_scale
    )

def main():
    generate_data()
    # build_data_from_json()


if __name__ == '__main__':
    main()
