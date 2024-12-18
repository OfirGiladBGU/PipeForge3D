from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


def main():
    # Parameters
    num_of_nodes = 50
    num_of_outputs = 1
    pcd_percentage = 1.0

    # Generate and plot the graphs
    gg = GraphGenerator()
    for i in range(num_of_outputs):
        nodes_data, position_to_node_map = gg.generate_random_3d_nodes_structure(num_of_nodes=num_of_nodes)
        graph = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)
        # print(nodes_data)
        # gg.plot_graph_3d(graph=graph)

        # Build the mesh
        mb = MeshBuilder()
        mesh = mb.build_mesh(graph=graph, output_filepath=f"output_{i + 1}.obj")
        mb.build_pcd(input_object=mesh, percentage=pcd_percentage, output_filepath=f"output_{i + 1}.pcd")


if __name__ == '__main__':
    main()
