import os
from tkinter import filedialog, messagebox
import shutil
import subprocess
import pyvista as pv


def generate_mesh(app, stl_path):
    """Generate OpenFOAM mesh using snappyHexMesh."""
    #stl_file = filedialog.askopenfilename(
    #    title="Select STL File for Mesh Generation",
    #    filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
    #)
    #if not stl_file:
    #    return  # User canceled
    stl_file = stl_path

    openfoam_dir = "openfoam_case"
    system_dir = os.path.join(openfoam_dir, "system")
    os.makedirs(system_dir, exist_ok=True)

    try:
        # Write snappyHexMeshDict
        snappyhexmesh_dict = f"""
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
    location    "system";
    object      snappyHexMeshDict;
}}

// Settings for snappyHexMesh
castellatedMesh true;
snap            true;
addLayers       false;

geometry
{{
    mesh
    {{
        type triSurfaceMesh;
        file "{os.path.basename(stl_file)}";
    }};
}};

castellatedMeshControls
{{
    maxLocalCells 100000;
    maxGlobalCells 2000000;
    minRefinementCells 10;
    nCellsBetweenLevels 3;

    refinementSurfaces
    {{
        mesh
        {{
            level (1 1);
        }};
    }};
}};
"""

        with open(os.path.join(system_dir, "snappyHexMeshDict"), "w") as f:
            f.write(snappyhexmesh_dict)

        # Copy STL file into OpenFOAM case directory
        tri_surface_dir = os.path.join(openfoam_dir, "constant/triSurface")
        os.makedirs(tri_surface_dir, exist_ok=True)
        shutil.copy(stl_file, os.path.join(tri_surface_dir, os.path.basename(stl_file)))

        # Run snappyHexMesh
        app.log_message("Running snappyHexMesh...")
        subprocess.run(["snappyHexMesh", "-case", openfoam_dir], check=True)
        app.log_message("Mesh generation completed successfully!")

        # Visualize the generated mesh
        visualize_mesh(app, openfoam_dir)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate mesh:\n{e}")


def visualize_mesh(app, openfoam_dir):
    """Visualize the generated mesh using PyVista."""
    try:
        mesh_file = os.path.join(openfoam_dir, "constant/polyMesh/faces")
        app.log_message("Visualizing the generated mesh...")
        mesh = pv.read(mesh_file)

        # Visualize with PyVista
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="lightblue")
        plotter.show()
    except Exception as e:
        app.log_message(f"Mesh visualization error: {e}")
