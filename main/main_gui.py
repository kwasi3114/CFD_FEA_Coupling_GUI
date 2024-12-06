import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from stl.stl_import import load_and_display_stl
from mesh.mesh_creation import generate_mesh
from mesh.blockmesh_generation import BlockMeshGenerator


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

        # BlockMesh generator instance
        self.block_mesh_generator = BlockMeshGenerator()

    def setup_stl_tab(self):
        """Set up the STL Viewer tab."""
        self.stl_canvas = tk.Canvas(self.stl_tab, bg="white", width=600, height=400)
        self.stl_canvas.pack(fill=tk.BOTH, expand=True)

        self.load_stl_button = ttk.Button(
            self.stl_tab, text="Load STL File", command=lambda: load_and_display_stl(self)
        )
        self.load_stl_button.pack(pady=10)

    def setup_mesh_tab(self):
        """Set up the Mesh Generation tab."""
        f = open("stl/stl_path.txt")

        self.generate_mesh_button = ttk.Button(
            self.mesh_tab,
            text="Generate OpenFOAM Mesh (snappyHexMesh)",
            command=lambda: generate_mesh(self, f.read()),
        )
        self.generate_mesh_button.pack(pady=10)

        # Add BlockMesh functionality
        self.block_mesh_button = ttk.Button(
            self.mesh_tab,
            text="Generate OpenFOAM Mesh (blockMesh)",
            command=self.configure_and_generate_blockmesh,
        )
        self.block_mesh_button.pack(pady=10)

        # Log area for messages
        self.log_frame = ttk.Frame(self.mesh_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """Log a message in the GUI."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def configure_and_generate_blockmesh(self):
        """Open a pop-up window for BlockMesh configuration and run the mesh generator."""
        def on_submit():
            try:
                # Get values from the fields
                vertices = vertices_field.get("1.0", tk.END).strip()
                blocks = blocks_field.get("1.0", tk.END).strip()
                edges = edges_field.get("1.0", tk.END).strip()
                boundary = boundary_field.get("1.0", tk.END).strip()
                merge_patch_pairs = mpp_field.get("1.0", tk.END).strip()

                # Update the BlockMesh dictionary
                #self.block_mesh_generator.vertices = vertices
                #self.block_mesh_generator.blocks = blocks
                #self.block_mesh_generator.boundary = boundary

                # Write and generate mesh
                self.block_mesh_generator.write_block_mesh_dict(
                    vertices=vertices,
                    blocks=blocks,
                    edges=edges,
                    boundary=boundary,
                    merge_patch_pairs=merge_patch_pairs
                )
                self.block_mesh_generator.run_block_mesh()
                self.log_message("BlockMesh generation completed successfully.")
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Pop-up window for BlockMesh configuration
        popup = tk.Toplevel(self.root)
        popup.title("Configure BlockMesh Parameters")
        popup.geometry("600x400")

        ttk.Label(popup, text="Vertices (e.g., (0 0 0) ...):").pack(anchor="w", padx=10)
        vertices_field = tk.Text(popup, height=5, width=70)
        vertices_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Blocks (e.g., hex ...):").pack(anchor="w", padx=10)
        blocks_field = tk.Text(popup, height=5, width=70)
        blocks_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Edges (e.g., arc ...):").pack(anchor="w", padx=10)
        edges_field = tk.Text(popup, height=5, width=70)
        edges_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Boundary conditions:").pack(anchor="w", padx=10)
        boundary_field = tk.Text(popup, height=5, width=70)
        boundary_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Merge Patch Pairs:").pack(anchor="w", padx=10)
        mpp_field = tk.Text(popup, height=5, width=70)
        mpp_field.pack(padx=10, pady=5)

        ttk.Button(popup, text="Submit", command=on_submit).pack(pady=10)

        popup.transient(self.root)  # Make the window modal
        popup.grab_set()
        self.root.wait_window(popup)


if __name__ == "__main__":
    root = tk.Tk()
    app = MeshGenerationApp(root)
    root.geometry("800x600")
    root.mainloop()
