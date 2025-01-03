import pyvista as pv
import meshio

# Read the MSH file using meshio
mesh = meshio.read("converted_mesh.msh")

# Convert to PyVista format
grid = pv.UnstructuredGrid(mesh.cells, mesh.cell_data, mesh.points)

# Plot the mesh
grid.plot()
