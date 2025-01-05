import json
import trimesh
import open3d as o3d

from graph_generator import GraphGenerator


class Visualizer:
    def __init__(self, data_filepath: str, graph_scale: int = 1):
        self.data_filepath = data_filepath
        self.graph_scale = graph_scale

    def visualize_graph(self):
        if self.data_filepath.endswith(".json"):
            with open(self.data_filepath, "r") as fp:
                nodes_data = json.load(fp=fp)

            gg = GraphGenerator()
            graph = gg.generate_graph_3d(nodes_data=nodes_data)
            gg.plot_graph_3d(graph=graph, scale=self.graph_scale)
        else:
            raise ValueError(f"Invalid data file: {self.data_filepath}")

    def visualize_mesh(self):
        mesh = trimesh.load(file_obj=self.data_filepath)
        mesh.show()

    def visualize_pcd(self):
        pcd = o3d.io.read_point_cloud(filename=self.data_filepath)
        o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Viewer")


def main():
    json_filepath = "output/01.json"
    visualizer = Visualizer(data_filepath=json_filepath)
    visualizer.visualize_graph()

    mesh_filepath = "output/01.obj"
    visualizer = Visualizer(data_filepath=mesh_filepath)
    visualizer.visualize_mesh()

    pcd_filepath = "output/01.pcd"
    visualizer = Visualizer(data_filepath=pcd_filepath)
    visualizer.visualize_pcd()


if __name__ == '__main__':
    main()
