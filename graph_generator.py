import json
import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple, List


class GraphGenerator:
    def __init__(self):
        # Parameters
        self.available_num_of_connections = [1, 2, 3, 4, 5, 6]
        self.num_of_connections_probabilities = [0.05, 0.5, 0.2, 0.1, 0.10, 0.05]
        self.coupler_elbow_probabilities = [0.8, 0.2]
        # TODO: Implement probabilities for the following connection types
        # self.tee_or_three_way_elbow_probabilities = [0.8, 0.2]
        # self.four_way_tee_or_four_way_elbow_probabilities = [0.8, 0.2]
        self.connection_types = ["x", "-x", "y", "-y", "z", "-z"]

    #####################
    # Utility functions #
    #####################
    def get_random_min_num_of_connections(self) -> int:
        min_num_of_connections = random.choices(
            population=self.available_num_of_connections,
            weights=self.num_of_connections_probabilities,
            k=1
        )
        return min_num_of_connections[0]

    def get_opposite_connection_type(self, connection_type: str) -> str:
        if connection_type not in self.connection_types:
            raise ValueError(f"Invalid connection type: {connection_type}")

        if "-" in connection_type:
            opposite_connection_type = connection_type[1:]
        else:
            opposite_connection_type = "-" + connection_type
        return opposite_connection_type

    @staticmethod
    def get_connection_type_node_position(node_position: Tuple[int, int, int],
                                          connection_type: str) -> Tuple[int, int, int]:
        deltas = {
            "x": (1, 0, 0),
            "-x": (-1, 0, 0),
            "y": (0, 1, 0),
            "-y": (0, -1, 0),
            "z": (0, 0, 1),
            "-z": (0, 0, -1),
        }

        if connection_type not in deltas:
            raise ValueError(f"Invalid connection type: {connection_type}")

        dx, dy, dz = deltas[connection_type]
        connection_type_node_position = (node_position[0] + dx, node_position[1] + dy, node_position[2] + dz)
        return connection_type_node_position

    def get_node_active_and_invalid_connection_lists(self,
                                                     node_position: Tuple[int, int, int],
                                                     nodes_data: dict,
                                                     position_to_node_map: dict) -> Tuple[List[str], List[str]]:
        active_connection_list = []
        invalid_connection_list = []

        for connection_type in self.connection_types:
            neighbor_node_position = self.get_connection_type_node_position(
                node_position=node_position,
                connection_type=connection_type
            )
            neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

            if neighbor_node_idx != -1:
                neighbor_connection_type = self.get_opposite_connection_type(connection_type=connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["active_connection_list"]:
                    active_connection_list.append(connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["invalid_connection_list"]:
                    invalid_connection_list.append(connection_type)

        return active_connection_list, invalid_connection_list

    def get_random_new_connection_types(self,
                                        min_num_of_connections: int,
                                        active_connection_list: List[str],
                                        invalid_connection_list: List[str]) -> List[str]:
        selectable_connection = set(self.connection_types) - set(active_connection_list) - set(invalid_connection_list)
        selectable_connection = list(selectable_connection)

        num_of_selectable_connections = len(selectable_connection)
        num_of_choices_available = min_num_of_connections - len(active_connection_list)

        # Min number of connections reached
        if num_of_choices_available <= 0:
            new_connection_types = []

        # Not enough selectable connections to reach min number of connections
        elif num_of_choices_available > num_of_selectable_connections:
            new_connection_types = selectable_connection

        # (Optional) Special case: select between Coupler and Elbow connection types
        elif num_of_choices_available == 1 and len(active_connection_list) == 1:
            opposite_connection = self.get_opposite_connection_type(connection_type=active_connection_list[0])

            # Check if an opposite connection and at least one other connection are selectable
            # (Coupler and Elbow connection types are selectable)
            if opposite_connection in selectable_connection and num_of_selectable_connections > 1:
                selected_option = random.choices(
                    population=["Coupler", "Elbow"],
                    weights=self.coupler_elbow_probabilities,
                    k=1
                )
                if selected_option[0] == "Coupler":
                    new_connection_types = [opposite_connection]
                else:  # Elbow
                    selectable_connection.remove(opposite_connection)
                    new_connection_types = random.sample(population=selectable_connection, k=1)

            # Either Coupler or Elbow connection is only selectable
            else:
                new_connection_types = random.sample(population=selectable_connection, k=1)

        # Randomly select new connections to reach min number of connections
        else:
            new_connection_types = random.sample(population=selectable_connection, k=num_of_choices_available)

        return new_connection_types

    ######################
    # Building functions #
    ######################
    def generate_random_3d_nodes_data(self, num_of_nodes: int, output_filepath=None) -> dict:
        current_num_of_nodes = 0
        nodes_data = {}
        position_to_node_map = {}

        node_position = (0, 0, 0)
        node_positions_queue = deque()
        node_positions_queue.append(node_position)
        current_num_of_nodes += 1

        for node_idx in range(num_of_nodes):
            # Check if there are no more nodes that can be added
            if not node_positions_queue:
                break

            # Pop next node in queue
            node_position = node_positions_queue.popleft()
            min_num_of_connections = self.get_random_min_num_of_connections()
            active_connection_list, invalid_connection_list = self.get_node_active_and_invalid_connection_lists(
                node_position=node_position,
                nodes_data=nodes_data,
                position_to_node_map=position_to_node_map
            )

            # Set new connections to the node
            new_connection_types = self.get_random_new_connection_types(
                min_num_of_connections=min_num_of_connections,
                active_connection_list=active_connection_list,
                invalid_connection_list=invalid_connection_list
            )

            # Add node to graph
            active_connection_list.extend(new_connection_types)
            invalid_connection_list = list(set(self.connection_types) - set(active_connection_list))
            nodes_data[node_idx] = {
                "position": node_position,
                "active_connection_list": active_connection_list,
                "invalid_connection_list": invalid_connection_list
            }
            position_to_node_map[node_position] = node_idx

            # Add new node potions to queue
            for new_connection_type in new_connection_types:
                new_node_position = self.get_connection_type_node_position(
                    node_position=node_position,
                    connection_type=new_connection_type
                )

                # Prevent adding the same node position twice
                conditions = [
                    position_to_node_map.get(new_node_position, -1) == -1,
                    new_node_position not in node_positions_queue,
                    current_num_of_nodes < num_of_nodes
                ]
                if all(conditions):
                    node_positions_queue.append(new_node_position)
                    current_num_of_nodes += 1

        if output_filepath is not None:
            with open(output_filepath, "w") as fp:
                json.dump(obj=nodes_data, fp=fp, indent=4)
        return nodes_data

    def generate_graph_3d(self, nodes_data: dict) -> nx.Graph:
        position_to_node_map = {node_data["position"]: node_idx for node_idx, node_data in nodes_data.items()}

        graph = nx.Graph()

        # Add nodes
        for node_idx, node_data in nodes_data.items():
            graph.add_node(node_idx, position=node_data["position"], connections=node_data["active_connection_list"])

        # Add edges
        for node_idx, node_data in nodes_data.items():
            for connection_type in node_data["active_connection_list"]:
                neighbor_node_position = self.get_connection_type_node_position(
                    node_position=node_data["position"],
                    connection_type=connection_type
                )
                neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

                if neighbor_node_idx != -1:
                    graph.add_edge(node_idx, neighbor_node_idx)

        return graph

    @staticmethod
    def plot_graph_3d(graph: nx.Graph, scale: int = 1, output_filepath=None):
        """
        Plot the 3D graph using matplotlib and display connections.

        Parameters:
            graph (networkx.Graph): A graph object.
            scale (int): A scale factor for the plot.
            output_filepath (str): An output file path to save the plot (if not provided: plt.show() will be executed).
        """
        positions = nx.get_node_attributes(graph, "position")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Draw edges
        for edge in graph.edges():
            x = [positions[edge[0]][0] * scale, positions[edge[1]][0] * scale]
            y = [positions[edge[0]][1] * scale, positions[edge[1]][1] * scale]
            z = [positions[edge[0]][2] * scale, positions[edge[1]][2] * scale]
            ax.plot(x, y, z, color="red", linewidth=1)

        # Draw nodes and labels
        for node, (x, y, z) in positions.items():
            x, y, z = x * scale, y * scale, z * scale
            ax.scatter(x, y, z, c="blue", s=25)
            ax.text(x, y, z, s=str(node), color="red", fontsize=8)

        if output_filepath is not None:
            plt.savefig(output_filepath)
        else:
            plt.show()


########
# Test #
########
def test():
    # Parameters
    num_of_nodes = 20
    scale = 1

    # Generate and plot the graph
    gg = GraphGenerator()
    nodes_data = gg.generate_random_3d_nodes_data(num_of_nodes=num_of_nodes)
    graph = gg.generate_graph_3d(nodes_data=nodes_data)
    gg.plot_graph_3d(graph=graph, scale=scale)


if __name__ == '__main__':
    test()
