from graph_generator import GraphGenerator
from mesh_builder import MeshBuilder


def main():
    # Parameters
    num_nodes = 20

    # Generate and plot the graph
    gg = GraphGenerator()
    nodes_data, position_to_node_map = gg.generate_random_3d_nodes_structure(num_nodes=num_nodes)
    G = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)
    # gg.plot_graph_3d(G=G)

    # Build the mesh
    mb = MeshBuilder()
    mb.build_mesh(G=G)


if __name__ == '__main__':
    main()
