import tkinter as tk
from tkinter import ttk
from stl.stl_import import load_and_display_stl
from mesh.mesh_creation import generate_mesh


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
            self.stl_tab, text="Load STL File", command=lambda: load_and_display_stl(self)
        )
        self.load_stl_button.pack(pady=10)

    def setup_mesh_tab(self):
        f = open("stl/stl_path.txt")

        self.generate_mesh_button = ttk.Button(
            self.mesh_tab, text="Generate OpenFOAM Mesh", command=lambda: generate_mesh(self, f.read())
        )
        self.generate_mesh_button.pack(pady=10)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = MeshGenerationApp(root)
    root.geometry("800x600")
    root.mainloop()
