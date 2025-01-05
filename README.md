# Pipes3DGenerator


## Description

This project is a Python 3D pipes generator for industrial applications. 
The script generates random graphs that can be converted into 3D models and point clouds of pipes, 
using the available kit of connection types meshes.


## Getting Started

1. Go to the [main.py](main.py) script and update the parameters of the `generate_pipes` function to your needs:
   1. `num_of_nodes` - the number of nodes in the random graph (each node represents a pipe connection).
   2. `num_of_outputs` - number of output pipes to generate.
   3. `graph_scale` - the scale of the output graph `.png` images. 
   4. `pcd_percentage` - the percentage of point to sample from the output 3D mesh to convert to a point cloud.
2. Run the script:
   ```bash
   python main.py
   ```

   
## Classes Breakdown

- `GraphGenerator` ([graph_generator.py](graph_generator.py)) - generates a random graph of the pipes model.
- `MeshBuilder` ([mesh_builder.py](mesh_builder.py)) - build the 3D mesh and point cloud of the pipes model from a given graph.
- `MeshBuilderTests` ([mesh_builder_tests.py](mesh_builder_tests.py)) - unit tests for the `MeshBuilder` class using the available kit of connection types meshes.
- `Visualizer` ([visualizer.py](visualizer.py)) - a tool to visualize the graph, 3D mesh and point cloud of a pipes model.


## Examples
