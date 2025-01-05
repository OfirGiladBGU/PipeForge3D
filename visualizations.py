import json
import trimesh
import open3d as o3d

from graph_generator import GraphGenerator


def visualize_graph_from_json(json_filepath: str, graph_scale: int):
    with open(json_filepath, "r") as fp:
        nodes_data = json.load(fp=fp)

    gg = GraphGenerator()
    graph = gg.generate_graph_3d(nodes_data=nodes_data)
    gg.plot_graph_3d(graph=graph, scale=graph_scale)


def visualize_mesh(mesh_filepath: str):
    mesh = trimesh.load(file_obj=mesh_filepath)
    mesh.show()


def visualize_pcd(pcd_filepath: str):
    pcd = o3d.io.read_point_cloud(filename=pcd_filepath)
    o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Viewer")


def main():
    json_filepath = "output/01.json"
    visualize_graph_from_json(json_filepath=json_filepath, graph_scale=1)

    mesh_filepath = "output/01.obj"
    visualize_mesh(mesh_filepath=mesh_filepath)

    pcd_filepath = "output/01.pcd"
    visualize_pcd(pcd_filepath=pcd_filepath)


if __name__ == '__main__':
    main()
