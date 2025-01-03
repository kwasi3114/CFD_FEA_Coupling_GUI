import pyvista as pv
import sys

def visualize_xdmf(xdmf_file):
    """
    Visualize a mesh stored in an XDMF file using PyVista.
    
    Args:
        xdmf_file (str): Path to the XDMF file.
    """
    try:
        # Read the mesh using PyVista
        mesh = pv.read(xdmf_file)
        
        # Check if the mesh was loaded correctly
        if mesh is None or mesh.n_points == 0:
            print("Error: The mesh is empty or invalid.")
            return
        
        # Create a PyVista plotter
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="cyan", show_edges=True, edge_color="black")
        plotter.add_axes()  # Add axes for orientation
        plotter.add_title("XDMF Mesh Visualization")
        
        # Show the plot
        plotter.show()
    except Exception as e:
        print(f"An error occurred while visualizing the XDMF file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize_xdmf.py <path_to_xdmf_file>")
        sys.exit(1)
    
    xdmf_file_path = sys.argv[1]
    print("File path: " + xdmf_file_path)
    visualize_xdmf(xdmf_file_path)


