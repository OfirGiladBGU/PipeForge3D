import random
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

from networkx.classes import neighbors

CONNECTION_TYPES = ["x", "-x", "y", "-y", "z", "-z"]


class Connections(Enum):
    Coupler = 1
    Elbow = 2
    Tee = 3
    Cross = 4
    AllDirections = 5


def get_random_num_of_connections(): # TODO: change to a more realistic distribution
    return random.randint(2, 6)


def get_random_new_connection_types(num_of_connections,
                                    active_connections,
                                    invalid_connections): # TODO: handle invalid connections
    selectable_connection = list(set(CONNECTION_TYPES) - set(active_connections))
    num_of_choices_available = num_of_connections - len(active_connections)

    if num_of_choices_available <= 0:
        new_connection_types = []
    else:
        new_connection_types = random.choices(selectable_connection, k=num_of_choices_available)
    return new_connection_types


def get_connection_type_node_position(node_position, connection_type):
    if connection_type == "x":
        return node_position[0] + 1, node_position[1], node_position[2]
    elif connection_type == "-x":
        return node_position[0] - 1, node_position[1], node_position[2]
    elif connection_type == "y":
        return node_position[0], node_position[1] + 1, node_position[2]
    elif connection_type == "-y":
        return node_position[0], node_position[1] - 1, node_position[2]
    elif connection_type == "z":
        return node_position[0], node_position[1], node_position[2] + 1
    elif connection_type == "-z":
        return node_position[0], node_position[1], node_position[2] - 1
    else:
        raise ValueError(f"Invalid connection type: {connection_type}")


def get_opposite_connection_type(connection_type):
    if connection_type == "x":
        return "-x"
    elif connection_type == "-x":
        return "x"
    elif connection_type == "y":
        return "-y"
    elif connection_type == "-y":
        return "y"
    elif connection_type == "z":
        return "-z"
    elif connection_type == "-z":
        return "z"
    else:
        raise ValueError(f"Invalid connection type: {connection_type}")


def get_node_active_and_invalid_connections(node_position, nodes_data, position_to_node_map):
    active_connections = []
    invalid_connections = []

    for connection_type in CONNECTION_TYPES:
        neighbor_node_position = get_connection_type_node_position(node_position, connection_type)
        neighbor_node_idx = position_to_node_map.get(neighbor_node_position, -1)

        if neighbor_node_idx != -1:
            neighbor_connection_type = get_opposite_connection_type(connection_type)

            if neighbor_connection_type in nodes_data[neighbor_node_idx]["active_connections"]:
                active_connections.append(connection_type)

            if neighbor_connection_type in nodes_data[neighbor_node_idx]["invalid_connections"]:
                invalid_connections.append(connection_type)

    return active_connections, invalid_connections


def generate_random_graph_3d(num_of_defined_nodes):
    G = nx.Graph()
    nodes_data = {}
    position_to_node_map = {}

    node_position = (0, 0, 0)
    node_positions_queue = deque()
    node_positions_queue.append(node_position)

    for node_idx in range(num_of_defined_nodes):
        if not node_positions_queue:
            break

        # Pop next node
        node_position = node_positions_queue.popleft()
        num_of_connections = get_random_num_of_connections()
        active_connections, invalid_connections = get_node_active_and_invalid_connections(
            node_position,
            nodes_data,
            position_to_node_map
        )

        # Get new connections
        new_connection_types = get_random_new_connection_types(
            num_of_connections,
            active_connections,
            invalid_connections
        )

        # Build nodes_data
        active_connections.extend(new_connection_types)
        invalid_connections = list(set(CONNECTION_TYPES) - set(active_connections))
        nodes_data[node_idx] = {
            "position": node_position,
            "active_connections": active_connections,
            "invalid_connections": invalid_connections
        }

        # Add new node potions to queue
        for new_connection_type in new_connection_types:
            new_node_position = get_connection_type_node_position(node_position, new_connection_type)
            new_node_idx = position_to_node_map.get(new_node_position, -1)

            if new_node_idx == -1:
                node_positions_queue.append(new_node_position)

    # return G, positions


def plot_graph_3d(G, positions):
    """
    Plot the 3D graph using matplotlib and display connections.

    Parameters:
        G (networkx.Graph): A graph object.
        positions (dict): A dictionary mapping nodes to 3D positions.
    """
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
        ax.scatter(x, y, z, c="blue", s=50)
        ax.text(x, y, z, f"{node}", color="red", fontsize=8)

    # Display edge labels
    for edge in G.edges():
        mid_x = (positions[edge[0]][0] + positions[edge[1]][0]) / 2
        mid_y = (positions[edge[0]][1] + positions[edge[1]][1]) / 2
        mid_z = (positions[edge[0]][2] + positions[edge[1]][2]) / 2
        ax.text(mid_x, mid_y, mid_z, f"{edge}", color="green", fontsize=6)

    plt.show()


# Parameters
num_nodes = 20

# Generate and plot the graph
G, positions = generate_random_graph_3d(num_nodes)
plot_graph_3d(G, positions)

# if __name__ == '__main__':
#     pass