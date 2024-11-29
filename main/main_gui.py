import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
from mpl_toolkits.mplot3d import Axes3D, art3d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_and_display_mesh():
    # Open file dialog to select an STL file
    file_path = filedialog.askopenfilename(
        title="Select an STL File",
        filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return  # User canceled the file selection

    try:
        # Load the STL file using trimesh
        mesh = trimesh.load(file_path)

        # Create a new figure for the plot
        figure = plt.Figure()
        axes = figure.add_subplot(111, projection='3d')
        
        # Extract mesh data for plotting
        vertices = mesh.vertices
        faces = mesh.faces

        # Create a Poly3DCollection from the faces
        collection = art3d.Poly3DCollection(vertices[faces], alpha=0.7, edgecolor='k')
        axes.add_collection3d(collection)

        # Auto scale the plot to fit the mesh
        scale = vertices.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
        
        # Set plot labels
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_zlabel("Z")

        # Embed the plot in the tkinter GUI
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load mesh file:\n{e}")

# Create the main application window
root = tk.Tk()
root.title("STL Mesh Viewer")

# Create a frame to hold the plot
frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True)

# Create a button to load the mesh
load_button = tk.Button(root, text="Import and Display Mesh", command=load_and_display_mesh)
load_button.pack(pady=10)

# Start the Tkinter main loop
root.geometry("800x600")
root.mainloop()
