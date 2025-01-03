import pyvista as pv

#reader = pv.XdmfReader('converted_mesh.xdmf')
mesh = pv.read('converted_mesh.xdmf')
print("Mesh accessed")
# Access data arrays
#print(mesh['your_data_array'])
