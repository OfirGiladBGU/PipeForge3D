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
        self.connection_types = ["x", "-x", "y", "-y", "z", "-z"]

        # Special cases parameters
        self.allow_special_cases = True
        self.coupler_elbow_probabilities = [0.8, 0.2]
        # TODO: Implement probabilities for the following connection types
        # self.tee_or_three_way_elbow_probabilities = [0.8, 0.2]
        # self.four_way_tee_or_four_way_elbow_probabilities = [0.8, 0.2]


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

    def get_node_opened_and_closed_connection_lists(self,
                                                    node_position: Tuple[int, int, int],
                                                    nodes_data: dict,
                                                    position_to_node_map: dict) -> Tuple[List[str], List[str]]:
        opened_connection_list = []
        closed_connection_list = []

        for connection_type in self.connection_types:
            neighbor_node_position = self.get_connection_type_node_position(
                node_position=node_position,
                connection_type=connection_type
            )
            neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

            if neighbor_node_idx != -1:
                neighbor_connection_type = self.get_opposite_connection_type(connection_type=connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["opened_connection_list"]:
                    opened_connection_list.append(connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["closed_connection_list"]:
                    closed_connection_list.append(connection_type)

        return opened_connection_list, closed_connection_list

    def handle_special_cases(self,
                             opened_connection_list: List[str],
                             selectable_connection: List[str],
                             num_of_choices_available: int,
                             num_of_selectable_connections: int) -> List[str]:
        # Special case: select between Coupler and Elbow connection types
        if num_of_choices_available == 1 and len(opened_connection_list) == 1:
            opposite_connection = self.get_opposite_connection_type(connection_type=opened_connection_list[0])

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

        # Special case: select between Tee or Three Way Elbow connection types

        # Special case: select between Four Way Tee or Four Way Elbow connection types

        else:
            new_connection_types = random.sample(population=selectable_connection, k=num_of_choices_available)

        return new_connection_types

    def get_random_new_connection_types(self,
                                        min_num_of_connections: int,
                                        opened_connection_list: List[str],
                                        closed_connection_list: List[str]) -> List[str]:
        selectable_connection = set(self.connection_types) - set(opened_connection_list) - set(closed_connection_list)
        selectable_connection = list(selectable_connection)

        num_of_selectable_connections = len(selectable_connection)
        num_of_choices_available = min_num_of_connections - len(opened_connection_list)

        # Min number of connections reached
        if num_of_choices_available <= 0:
            new_connection_types = []

        # Not enough selectable connections to reach min number of connections
        elif num_of_choices_available > num_of_selectable_connections:
            new_connection_types = selectable_connection

        elif self.allow_special_cases is True:
            new_connection_types = self.handle_special_cases(
                opened_connection_list=opened_connection_list,
                selectable_connection=selectable_connection,
                num_of_selectable_connections=num_of_selectable_connections,
                num_of_choices_available=num_of_choices_available,
            )

        # Randomly select new connections to reach min number of connections
        else:
            new_connection_types = random.sample(population=selectable_connection, k=num_of_choices_available)

        return new_connection_types

    def resolve_node_cycles(self,
                            node_position: Tuple[int, int, int],
                            opened_connection_list: List[str],
                            closed_connection_list: List[str],
                            position_to_node_map: dict,
                            nodes_data: dict) -> Tuple[List[str], List[str]]:
        # Check if the node has more than one open connection
        if len(opened_connection_list) > 1:
            # Randomly select a connection to keep
            new_opened_connection_list = random.choices(
                population=opened_connection_list,
                k=1
            )

            # Move the disabled connections to the closed connections
            disabled_connection_list = list(set(opened_connection_list) - set(new_opened_connection_list))
            opened_connection_list = new_opened_connection_list
            for connection_type in disabled_connection_list:
                # Add the connection to the closed connections
                closed_connection_list.append(connection_type)

                # Remove the connection from the neighbor node
                neighbor_node_position = self.get_connection_type_node_position(
                    node_position=node_position,
                    connection_type=connection_type
                )
                neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)
                if neighbor_node_idx != -1:
                    neighbor_connection_type = self.get_opposite_connection_type(connection_type=connection_type)
                    nodes_data[neighbor_node_idx]["opened_connection_list"].remove(neighbor_connection_type)
                    nodes_data[neighbor_node_idx]["closed_connection_list"].append(neighbor_connection_type)
                else:
                    raise ValueError(f"[BUG] Neighbor node index: {neighbor_node_idx} should exists!")
        else:
            pass

        return opened_connection_list, closed_connection_list

    ######################
    # Building functions #
    ######################
    def generate_random_3d_nodes_data(self, num_of_nodes: int, tree_mode: bool = False, output_filepath=None) -> dict:
        current_num_of_nodes = 0
        nodes_data = {}
        position_to_node_map = {}

        node_position = (0, 0, 0)
        node_positions_queue = deque()
        node_positions_queue.append(node_position)
        current_num_of_nodes += 1

        for node_idx in range(num_of_nodes):
            node_idx = str(node_idx)

            # Check if there are no more nodes that can be added
            if not node_positions_queue:
                break

            # Pop next node in queue
            node_position = node_positions_queue.popleft()
            min_num_of_connections = self.get_random_min_num_of_connections()
            opened_connection_list, closed_connection_list = self.get_node_opened_and_closed_connection_lists(
                node_position=node_position,
                nodes_data=nodes_data,
                position_to_node_map=position_to_node_map
            )

            if tree_mode is True:
                opened_connection_list, closed_connection_list = self.resolve_node_cycles(
                    node_position=node_position,
                    opened_connection_list=opened_connection_list,
                    closed_connection_list=closed_connection_list,
                    position_to_node_map=position_to_node_map,
                    nodes_data=nodes_data
                )

            # Set new connections to the node
            new_connection_types = self.get_random_new_connection_types(
                min_num_of_connections=min_num_of_connections,
                opened_connection_list=opened_connection_list,
                closed_connection_list=closed_connection_list
            )

            # Add node to graph
            opened_connection_list.extend(new_connection_types)
            closed_connection_list = list(set(self.connection_types) - set(opened_connection_list))
            nodes_data[node_idx] = {
                "position": node_position,
                "opened_connection_list": opened_connection_list,
                "closed_connection_list": closed_connection_list
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
            # Notice: Cast the node positions to list to save them in the json file
            for node_idx, node_data in nodes_data.items():
                nodes_data[node_idx]["position"] = list(node_data["position"])
            with open(output_filepath, "w") as fp:
                json.dump(obj=nodes_data, fp=fp, indent=4)
        return nodes_data

    def generate_graph_3d(self, nodes_data: dict) -> nx.Graph:
        # Notice: Cast the node positions to tuple to use them as keys in the dictionary (json doesn't support tuples)
        for node_idx, node_data in nodes_data.items():
            nodes_data[node_idx]["position"] = tuple(node_data["position"])
        position_to_node_map = {node_data["position"]: node_idx for node_idx, node_data in nodes_data.items()}

        graph = nx.Graph()

        # Add nodes
        for node_idx, node_data in nodes_data.items():
            graph.add_node(node_idx, position=node_data["position"], connections=node_data["opened_connection_list"])

        # Add edges
        for node_idx, node_data in nodes_data.items():
            for connection_type in node_data["opened_connection_list"]:
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
            plt.close(fig)
        else:
            plt.show()


########
# Test #
########
def test():
    # Parameters
    num_of_nodes = 20
    scale = 1
    tree_mode = True

    # Generate and plot the graph
    gg = GraphGenerator()
    nodes_data = gg.generate_random_3d_nodes_data(num_of_nodes=num_of_nodes, tree_mode=tree_mode)
    graph = gg.generate_graph_3d(nodes_data=nodes_data)
    gg.plot_graph_3d(graph=graph, scale=scale)


if __name__ == '__main__':
    test()
