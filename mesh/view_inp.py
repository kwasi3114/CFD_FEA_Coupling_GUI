import pyvista as pv
import meshio

# Read the .inp file
mesh = meshio.read("main.inp")

# Convert to PyVista format
points = mesh.points
faces = mesh.cells_dict.get("triangle")
if faces is not None:
    # Flatten faces for PyVista
    faces = faces.reshape(-1)
    pv_mesh = pv.PolyData(points, faces)

    # Plot
    plotter = pv.Plotter()
    plotter.add_mesh(pv_mesh, show_edges=True, color="white")
    plotter.show()

