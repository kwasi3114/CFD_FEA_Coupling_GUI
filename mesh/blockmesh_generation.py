import os
import subprocess


class BlockMeshGenerator:
    def __init__(self, case_dir="blockmesh_case"):
        self.case_dir = case_dir
        self.system_dir = os.path.join(self.case_dir, "system")
        self.constant_dir = os.path.join(self.case_dir, "constant")
        self.poly_mesh_dir = os.path.join(self.constant_dir, "polyMesh")
        self.block_mesh_dict_path = os.path.join(self.system_dir, "blockMeshDict")
        self.create_case_directories()

    def create_case_directories(self):
        """Create the necessary OpenFOAM case directory structure."""
        os.makedirs(self.system_dir, exist_ok=True)
        os.makedirs(self.poly_mesh_dir, exist_ok=True)

    def write_block_mesh_dict(self):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        block_mesh_dict = """
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  8                                     |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*--------------------------------------------------------------------------*/

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

// Define vertices of the block
vertices
(
    (0 0 0)       // Vertex 0
    (1 0 0)       // Vertex 1
    (1 1 0)       // Vertex 2
    (0 1 0)       // Vertex 3
    (0 0 1)       // Vertex 4
    (1 0 1)       // Vertex 5
    (1 1 1)       // Vertex 6
    (0 1 1)       // Vertex 7
);

// Define a single block using hexahedral cells
blocks
(
    hex (0 1 2 3 4 5 6 7) (10 10 10) simpleGrading (1 1 1)
);

// Boundary conditions
edges
(
);

// Patch definitions
boundary
(
    inlet
    {
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (1 5 6 2)
        );
    }
    walls
    {
        type wall;
        faces
        (
            (0 1 5 4)
            (2 3 7 6)
            (0 3 2 1)
            (4 5 6 7)
        );
    }
);

// Default internal field
mergePatchPairs
(
);
"""
        with open(self.block_mesh_dict_path, "w") as f:
            f.write(block_mesh_dict)

    def run_block_mesh(self):
        """Run the blockMesh utility to generate the mesh."""
        try:
            print("Running blockMesh...")
            subprocess.run(["blockMesh", "-case", self.case_dir], check=True)
            print("Mesh generation completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error running blockMesh: {e}")

    def visualize_mesh(self):
        """Visualize the generated mesh using pyvista."""
        import pyvista as pv

        try:
            mesh_file = os.path.join(self.poly_mesh_dir, "faces")
            if not os.path.exists(mesh_file):
                raise FileNotFoundError(f"Mesh file not found: {mesh_file}")

            print("Visualizing the generated mesh...")
            mesh = pv.read(mesh_file)
            plotter = pv.Plotter()
            plotter.add_mesh(mesh, color="lightblue", show_edges=True)
            plotter.show()
        except Exception as e:
            print(f"Failed to visualize mesh: {e}")


if __name__ == "__main__":
    generator = BlockMeshGenerator()
    generator.write_block_mesh_dict()
    generator.run_block_mesh()
    # Uncomment the following line to visualize the mesh
    # generator.visualize_mesh()
