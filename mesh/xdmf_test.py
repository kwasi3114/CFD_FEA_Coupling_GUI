import pyvista as pv
import xdmf

# Read the XDMF file
reader = xdmf.XdmfReader()
reader.open('converted_mesh.xdmf')
grid = reader.read()

# Plot the data
plotter = pv.Plotter()
plotter.add_mesh(grid)
plotter.show()
