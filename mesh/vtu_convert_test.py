import meshio

# Read the original VTU file
mesh = meshio.read("converted_mesh.vtu")

# Filter out polygons or convert them
cells = {key: value for key, value in mesh.cells_dict.items() if key != "polygon"}

# Create a new mesh object
processed_mesh = meshio.Mesh(points=mesh.points, cells=cells)

# Write to the ABAQUS format
#meshio.write("main.inp", processed_mesh)
meshio.write("converted_mesh.msh", processed_mesh)
