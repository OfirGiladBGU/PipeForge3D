import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


class GraphGenerator:
    def __init__(self):
        # Parameters
        self.available_num_of_connections = [2, 3, 4, 5, 6]
        self.num_of_connections_probabilities = [0.5, 0.2, 0.1, 0.15, 0.05]
        self.coupler_elbow_probabilities = [0.8, 0.2]
        self.connection_types = ["x", "-x", "y", "-y", "z", "-z"]
        self.nodes_distance = 1

    #####################
    # Utility functions #
    #####################
    def get_random_min_num_of_connections(self):
        min_num_of_connections = random.choices(
            population=self.available_num_of_connections,
            weights=self.num_of_connections_probabilities,
            k=1
        )
        return min_num_of_connections[0]

    def get_opposite_connection_type(self, connection_type: str):
        if connection_type not in self.connection_types:
            raise ValueError(f"Invalid connection type: {connection_type}")

        if "-" in connection_type:
            opposite_connection_type = connection_type[1:]
        else:
            opposite_connection_type = "-" + connection_type
        return opposite_connection_type

    def get_connection_type_node_position(self, node_position: tuple, connection_type: str):
        deltas = {
            "x": (self.nodes_distance, 0, 0),
            "-x": (-self.nodes_distance, 0, 0),
            "y": (0, self.nodes_distance, 0),
            "-y": (0, -self.nodes_distance, 0),
            "z": (0, 0, self.nodes_distance),
            "-z": (0, 0, -self.nodes_distance),
        }

        if connection_type not in deltas:
            raise ValueError(f"Invalid connection type: {connection_type}")

        dx, dy, dz = deltas[connection_type]
        return node_position[0] + dx, node_position[1] + dy, node_position[2] + dz

    def get_node_active_and_invalid_connections(self,
                                                node_position: tuple,
                                                nodes_data: dict,
                                                position_to_node_map: dict) -> tuple:
        active_connections = []
        invalid_connections = []

        for connection_type in self.connection_types:
            neighbor_node_position = self.get_connection_type_node_position(
                node_position=node_position,
                connection_type=connection_type
            )
            neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

            if neighbor_node_idx != -1:
                neighbor_connection_type = self.get_opposite_connection_type(connection_type=connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["active_connections"]:
                    active_connections.append(connection_type)

                if neighbor_connection_type in nodes_data[neighbor_node_idx]["invalid_connections"]:
                    invalid_connections.append(connection_type)

        return active_connections, invalid_connections

    def get_random_new_connection_types(self,
                                        min_num_of_connections: int,
                                        active_connections: list,
                                        invalid_connections: list) -> list:
        selectable_connection = list(set(self.connection_types) - set(active_connections) - set(invalid_connections))
        num_of_selectable_connections = len(selectable_connection)
        num_of_choices_available = min_num_of_connections - len(active_connections)

        # Min number of connections reached
        if num_of_choices_available <= 0:
            new_connection_types = []

        # Not enough selectable connections to reach min number of connections
        elif num_of_choices_available > num_of_selectable_connections:
            new_connection_types = selectable_connection

        # (Optional) Special case: select between Coupler and Elbow connection types
        elif num_of_choices_available == 1 and len(active_connections) == 1:
            opposite_connection = self.get_opposite_connection_type(connection_type=active_connections[0])

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
    def generate_random_3d_nodes_structure(self, num_nodes: int):
        current_num_of_nodes = 0
        nodes_data = {}
        position_to_node_map = {}

        node_position = (0, 0, 0)
        node_positions_queue = deque()
        node_positions_queue.append(node_position)
        current_num_of_nodes += 1

        for node_idx in range(num_nodes):
            # Check if there are no more nodes that can be added
            if not node_positions_queue:
                break

            # Pop next node in queue
            node_position = node_positions_queue.popleft()
            min_num_of_connections = self.get_random_min_num_of_connections()
            active_connections, invalid_connections = self.get_node_active_and_invalid_connections(
                node_position=node_position,
                nodes_data=nodes_data,
                position_to_node_map=position_to_node_map
            )

            # Set new connections to the node
            new_connection_types = self.get_random_new_connection_types(
                min_num_of_connections=min_num_of_connections,
                active_connections=active_connections,
                invalid_connections=invalid_connections
            )

            # Add node to graph
            active_connections.extend(new_connection_types)
            invalid_connections = list(set(self.connection_types) - set(active_connections))
            nodes_data[node_idx] = {
                "position": node_position,
                "active_connections": active_connections,
                "invalid_connections": invalid_connections
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
                    current_num_of_nodes < num_nodes
                ]
                if all(conditions):
                    node_positions_queue.append(new_node_position)
                    current_num_of_nodes += 1

        return nodes_data, position_to_node_map

    def generate_graph_3d(self, nodes_data: dict, position_to_node_map: dict) -> nx.Graph:
        G = nx.Graph()

        # Add nodes
        for node_idx, node_data in nodes_data.items():
            G.add_node(node_idx, position=node_data["position"], connections=node_data["active_connections"])

        # Add edges
        for node_idx, node_data in nodes_data.items():
            for connection_type in node_data["active_connections"]:
                neighbor_node_position = self.get_connection_type_node_position(
                    node_position=node_data["position"],
                    connection_type=connection_type
                )
                neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

                if neighbor_node_idx != -1:
                    G.add_edge(node_idx, neighbor_node_idx)

        return G

    @staticmethod
    def plot_graph_3d(G: nx.Graph):
        """
        Plot the 3D graph using matplotlib and display connections.

        Parameters:
            G (networkx.Graph): A graph object.
        """
        positions = nx.get_node_attributes(G, "position")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Draw edges
        for edge in G.edges():
            x = [positions[edge[0]][0], positions[edge[1]][0]]
            y = [positions[edge[0]][1], positions[edge[1]][1]]
            z = [positions[edge[0]][2], positions[edge[1]][2]]
            ax.plot(x, y, z, color="red", linewidth=1)

        # Draw nodes and labels
        for node, (x, y, z) in positions.items():
            ax.scatter(x, y, z, c="blue", s=25)
            ax.text(x, y, z, s=str(node), color="red", fontsize=8)

        plt.show()


def main():
    # Parameters
    num_nodes = 20

    # Generate and plot the graph
    gg = GraphGenerator()
    nodes_data, position_to_node_map = gg.generate_random_3d_nodes_structure(num_nodes=num_nodes)
    G = gg.generate_graph_3d(nodes_data=nodes_data, position_to_node_map=position_to_node_map)
    gg.plot_graph_3d(G=G)


if __name__ == '__main__':
    main()
