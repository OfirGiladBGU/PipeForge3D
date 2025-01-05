# Pipes3DGenerator


## Description

This project is a Python 3D pipes generator for industrial applications. \
The script generates random graphs that can be converted into 3D models and point clouds of pipes, 
using the available kit of connection types meshes.


## Getting Started

1. Go to the [main.py](main.py) script and update the parameters of the `generate_data` function to your needs:
   1. `num_of_nodes` - the number of nodes in the random graph (each node represents a pipe connection).
   2. `num_of_outputs` - number of output pipe models to generate.
   3. `graph_scale` - the scale length of the edges in the output graph `.png` images.
   4. `mesh_dir` - the directory of the 3D mesh parts to use to build the mesh.
   5. `mesh_scale` - the scale length of the 3D mesh parts `.obj` files (for example: `Coupler` length).
   6. `pcd_use_sample_method` - whether to use the surface sample method or take the mesh points to generate the point cloud file.
   7. `pcd_points_to_sample` - the `percentage` or `number` of points to sample from the output 3D mesh to convert to a point cloud file.
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
