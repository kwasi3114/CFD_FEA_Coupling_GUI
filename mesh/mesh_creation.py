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
    print("STL Path: " + stl_path)
    stl_file = stl_path.split("/")[-1]
    emesh_file = stl_file.replace(".stl", ".eMesh")


    openfoam_dir = "openfoam_case"
    system_dir = os.path.join(openfoam_dir, "system")
    constant_dir = os.path.join(openfoam_dir, "constant")
    trisurface_dir = os.path.join(constant_dir, "triSurface")

    stl_dir = os.path.join(constant_dir, stl_file)
    emesh_dir = os.path.join(constant_dir, emesh_file)

    os.makedirs(system_dir, exist_ok=True)
    os.makedirs(trisurface_dir, exist_ok=True)

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
mergeTolerance 1e-6;

geometry
{{
    {stl_file}
    {{
        type triSurfaceMesh;
        name stl;

    }};

    box
    {{
        type searchableBox;
        min (-10 -10 -10);
        max (10 10 10);
    }};

    sphere
    {{
        type searchableSphere;
        centre (0 0 0);
        radius 15.0;

    }};
}};

castellatedMeshControls
{{
    maxLocalCells 100000;
    maxGlobalCells 2000000;
    minRefinementCells 0;
    nCellsBetweenLevels 1;

    resolveFeatureAngle 30;
    planarAngle 30;
    allowFreeStandingZoneFaces true;

    features
    (
        {{
            file {emesh_file};
            level 2;
        }}
    );

    refinementSurfaces
    {{
        stl
        {{
            level (1 1);
        }}

        sphere
        {{
            level (1 1);
            faceZone face_inner;
            cellZone cell_inner;
            cellZoneInside inside;
        }}
    }}

    refinementRegions
    {{
        box
        {{
            mode inside;
            levels ((1 1));
        }}
    }}

    locationInMesh (0.0 0.0 0.25);
}};

snapControls
{{
    nSmoothPatch 3;
    tolerance 2.0;
    nSolveIter 30;
    nRelaxIter 5;

        nFeatureSnapIter 10;
        implicitFeatureSnap false;
        explicitFeatureSnap true;
        multiRegionFeatureSnap false;
}};

addLayersControls
{{
    relativeSizes true;
    expansionRatio 1.0;
    finalLayerThickness 0.3;
    minThickness 0.25;

    layers
    {{

    }}
}};

meshQualityControls
{{
    maxNonOrtho 75;
    maxBoundarySkewness 20;
    maxInternalSkewness 4;
    maxConcave 80;
    minVol 1.00E-13;
    minTetQuality 1e15;
    minArea -1;
    minTwist 0.02;
    minDeterminant 0.001;
    minFaceWeight 0.05;
    minVolRatio 0.01;
    minTriangleTwist -1;
    minFlatness 0.5;
    nSmoothScale 4;
    errorReduction 0.75;
}};
"""

        with open(os.path.join(system_dir, "snappyHexMeshDict"), "w") as f:
            f.write(snappyhexmesh_dict)
        
        print("Wrote snappyHexMeshDict")

        # Copy STL file into OpenFOAM case directory
        #tri_surface_dir = os.path.join(openfoam_dir, "constant/triSurface")
        #os.makedirs(tri_surface_dir, exist_ok=True)
        #shutil.copy(stl_file, os.path.join(tri_surface_dir, os.path.basename(stl_file)))
        shutil.copy(stl_path, stl_dir)

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
