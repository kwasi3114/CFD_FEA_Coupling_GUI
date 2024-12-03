import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import pyvista as pv
import shutil


class MeshGenerationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STL Viewer and Mesh Generator")

        # Configure the main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add STL Viewer tab
        self.stl_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stl_tab, text="STL Viewer")
        self.setup_stl_tab()

        # Add Mesh Generation tab
        self.mesh_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.mesh_tab, text="Mesh Generator")
        self.setup_mesh_tab()

    def setup_stl_tab(self):
        """Set up the STL Viewer tab."""
        self.stl_canvas = tk.Canvas(self.stl_tab, bg="white", width=600, height=400)
        self.stl_canvas.pack(fill=tk.BOTH, expand=True)

        self.load_stl_button = ttk.Button(
            self.stl_tab, text="Load STL File", command=self.load_and_display_stl
        )
        self.load_stl_button.pack(pady=10)

    def setup_mesh_tab(self):
        """Set up the Mesh Generation tab."""
        self.generate_mesh_button = ttk.Button(
            self.mesh_tab, text="Generate OpenFOAM Mesh", command=self.generate_mesh
        )
        self.generate_mesh_button.pack(pady=10)

        self.log_frame = ttk.Frame(self.mesh_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def load_and_display_stl(self):
        """Load and display an STL file."""
        file_path = filedialog.askopenfilename(
            title="Select an STL File", filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )

        if not file_path:
            return  # User canceled

        try:
            self.log_message(f"Loading STL file: {file_path}")
            mesh = pv.read(file_path)

            # Display STL file in PyVista plotter
            plotter = pv.Plotter(window_size=(600, 400), off_screen=True)
            plotter.add_mesh(mesh, color="lightblue")
            plotter.add_axes()
            plotter.view_isometric()

            # Display in the canvas
            img = plotter.screenshot()
            self.display_image_in_canvas(img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load STL file:\n{e}")

    def display_image_in_canvas(self, img):
        """Display an image in the Tkinter canvas."""
        from PIL import Image, ImageTk

        img = Image.fromarray(img)
        self.canvas_image = ImageTk.PhotoImage(img)
        self.stl_canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

    def generate_mesh(self):
        """Generate OpenFOAM mesh using snappyHexMesh."""
        stl_file = filedialog.askopenfilename(
            title="Select STL File for Mesh Generation",
            filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )
        if not stl_file:
            return  # User canceled

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
            self.log_message("Running snappyHexMesh...")
            subprocess.run(["snappyHexMesh", "-case", openfoam_dir], check=True)
            self.log_message("Mesh generation completed successfully!")

            # Visualize the generated mesh
            self.visualize_mesh(openfoam_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate mesh:\n{e}")

    def visualize_mesh(self, openfoam_dir):
        """Visualize the generated mesh using PyVista."""
        try:
            mesh_file = os.path.join(openfoam_dir, "constant/polyMesh/faces")
            self.log_message("Visualizing the generated mesh...")
            mesh = pv.read(mesh_file)

            # Visualize with PyVista
            plotter = pv.Plotter()
            plotter.add_mesh(mesh, color="lightblue")
            plotter.show()
        except Exception as e:
            self.log_message(f"Mesh visualization error: {e}")

    def log_message(self, message):
        """Log a message in the GUI."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MeshGenerationApp(root)
    root.geometry("800x600")
    root.mainloop()
