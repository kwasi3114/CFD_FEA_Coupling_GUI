import os
from tkinter import filedialog, messagebox
import pyvista as pv
from PIL import Image, ImageTk
import subprocess
import meshio

def load_and_display_stl(app):
    """Load and display an STL file."""
    file_path = filedialog.askopenfilename(
        title="Select an STL File", filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
    )

    if not file_path:
        return  # User canceled

    try:
        app.log_message(f"Loading STL file: {file_path}")
        #mesh = pv.read(file_path)
        orig_stl = pv.read(file_path)
        stl_bounds = orig_stl.bounds
        #write_path(file_path)

        #center STL file
        stl_center = [(stl_bounds[1] + stl_bounds[0]) / 2,
                      (stl_bounds[3] + stl_bounds[2]) / 2,
                      (stl_bounds[5] + stl_bounds[4]) / 2]

        scale_factors = (0.1, 0.1, 0.1)
        translation_vector = (-stl_center[0], -stl_center[1], -stl_center[2])

        scale_arg = f"({scale_factors[0]} {scale_factors[1]} {scale_factors[2]})"
        translate_arg = f"({translation_vector[0]} {translation_vector[1]} {translation_vector[2]})"

        output_path = file_path.replace(".stl", "_translated.stl")

        command = [
            "surfaceTransformPoints",
            "-scale", scale_arg,
            "-translate", translate_arg,
            file_path,
            output_path
        ]

        subprocess.run(command, check=True)
        print(f"STL file successfully transformed: {output_path}")
        
        # Use meshio to convert the transformed STL file to XDMF
        xdmf_path = output_path.replace(".stl", ".xdmf")
        convert_command = ["meshio", "convert", output_path, xdmf_path]
        
        try:
            subprocess.run(convert_command, check=True)
            print(f"STL file successfully converted to XDMF: {xdmf_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during mesh conversion: {e}")

        mesh = pv.read(output_path)
        write_path(output_path)

        #stl_filename = output_path.split("/")[-1]
        #write_surface_feature_extract_dict(stl_filename)
        #run_surface_feature_extract()

        # Display STL file in PyVista plotter
        plotter = pv.Plotter(window_size=(600, 400), off_screen=True)
        plotter.add_mesh(mesh, color="lightblue")
        plotter.add_axes()
        plotter.view_isometric()

        # Display in the canvas
        img = plotter.screenshot()
        display_image_in_canvas(app, img)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load STL file:\n{e}")


def display_image_in_canvas(app, img):
    """Display an image in the Tkinter canvas."""
    img = Image.fromarray(img)
    app.canvas_image = ImageTk.PhotoImage(img)
    app.stl_canvas.create_image(0, 0, anchor="nw", image=app.canvas_image)


def write_path(file_path):
    f = open("stl/stl_path.txt", "w")
    f.write(file_path)
    f.close()

def write_surface_feature_extract_dict(stl_file):
    """
    Writes the surfaceFeatureExtractDict file to the specified system folder.

    Parameters:
    stl_file (str): The name of the STL file to be used.
    system_folder (str): The folder where the surfaceFeatureExtractDict will be created.
    """
    import os 

    openfoam_dir = "openfoam_case"
    system_dir = os.path.join(openfoam_dir, "system")
    os.makedirs(system_dir, exist_ok=True)
    
    # Path to the surfaceFeatureExtractDict file
    dict_path = os.path.join(system_dir, "surfaceFeatureExtractDict")
    
    # Content of the surfaceFeatureExtractDict
    dict_content = f"""\
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.3.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      surfaceFeatureExtractDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

{stl_file}
{{
    // How to obtain raw features (extractFromFile || extractFromSurface)
    extractionMethod    extractFromSurface;

    extractFromSurfaceCoeffs
    {{
        // Mark edges whose adjacent surface normals are at an angle less
        // than includedAngle as features
        // - 0  : selects no edges
        // - 180: selects all edges
        includedAngle   150;
    }}

    // Write options

        // Write features to obj format for postprocessing
        writeObj                yes;
}}
// ************************************************************************* //
"""
    
    # Write the dictionary file
    with open(dict_path, "w") as file:
        file.write(dict_content)
    
    print(f"surfaceFeatureExtractDict written to {dict_path}")

def run_surface_feature_extract():
    """
    Runs the surfaceFeatureExtract command.
    """
    try:
        openfoam_dir = "openfoam_case"
        subprocess.run(["surfaceFeatureExtract", "-case", openfoam_dir], check=True)
        print("surfaceFeatureExtract completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error while running surfaceFeatureExtract:", e)
