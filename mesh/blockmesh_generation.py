import os
import subprocess


class BlockMeshGenerator:
    def __init__(self, case_dir="openfoam_case"):
        self.case_dir = case_dir
        self.system_dir = os.path.join(self.case_dir, "system")
        self.constant_dir = os.path.join(self.case_dir, "constant")
        self.poly_mesh_dir = os.path.join(self.constant_dir, "polyMesh")
        self.block_mesh_dict_path = os.path.join(self.system_dir, "blockMeshDict")
        self.create_case_directories()
        
        
        #openfoam_dir = "openfoam_case"
        #system_dir = os.path.join(openfoam_dir, "system")
        #os.makedirs(system_dir, exist_ok=True)

    def create_case_directories(self):
        """Create the necessary OpenFOAM case directory structure."""
        os.makedirs(self.system_dir, exist_ok=True)
        os.makedirs(self.poly_mesh_dir, exist_ok=True)

    def write_block_mesh_dict(self, vertices, blocks, edges, boundary, merge_patch_pairs):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        block_mesh_dict = f"""
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  8                                     |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*--------------------------------------------------------------------------*/

FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

// Define vertices of the block
vertices
(
    {vertices}
);

// Define a single block using hexahedral cells
blocks
(
    {blocks}
);

// Boundary conditions
edges
(
    {edges}
);

// Patch definitions
boundary
(
    {boundary}
);

// Default internal field
mergePatchPairs
(
    {merge_patch_pairs}
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

            print("Converting mesh to VTK format...")
            subprocess.run(["foamToVTK", "-case", self.case_dir], check=True)
            print("Conversion to VTK format completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error running blockMesh: {e}")

    def visualize_mesh(self, stl_file):
        """Visualize the generated mesh using pyvista."""
        import pyvista as pv

        try:
            #mesh_file = os.path.join(self.poly_mesh_dir, "faces")
            #if not os.path.exists(mesh_file):
            #    raise FileNotFoundError(f"Mesh file not found: {mesh_file}")
            vtk_dir = os.path.join(self.case_dir, "VTK")
            vtk_file = os.path.join(vtk_dir, "openfoam_case_0.vtm")
            #vtk_file = os.path.join(vtk_dir, "internal.vtk")

            if not os.path.exists(vtk_file):
                raise FileNotFoundError(f"VTK file not found: {vtk_file}")

            print("Visualizing the generated mesh...")
            background_mesh = pv.read(vtk_file)
            stl_mesh = pv.read(stl_file)
            plotter = pv.Plotter()

            plotter.add_mesh(stl_mesh, color="gray", opacity=0.5, label="STL Geometry")
            plotter.add_mesh(
                background_mesh,
                color="lightblue",
                opacity=0.7,
                show_edges=True,
                edge_color="blue",
                label="Generated Mesh",
            )
            #plotter.add_mesh(background_mesh, color="lightblue", show_edges=True, opacity=0.7)  # Semi-transparent

            plotter.add_legend()
            plotter.show()

            #print("Visualizing the generated mesh...")
            #mesh = pv.read(mesh_file)
            #plotter = pv.Plotter()
            #plotter.add_mesh(mesh, color="lightblue", show_edges=True)
            #plotter.show()
        except Exception as e:
            print(f"Failed to visualize mesh: {e}")


if __name__ == "__main__":
    generator = BlockMeshGenerator()
    generator.write_block_mesh_dict()
    generator.run_block_mesh()
    # Uncomment the following line to visualize the mesh
    # generator.visualize_mesh()
