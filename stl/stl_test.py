import trimesh

#file_path = r'C:\Users\kwasi\Downloads\stl_test.stl'
file_path = r'/home/kwasi_dp/CFD_FEA_Coupling_GUI/stl/tesla.stl'

try:
    # Load the STL file
    mesh = trimesh.load(file_path)
    print("STL file loaded successfully!")
    print(mesh)
    
    # Visualize the mesh
    mesh.show()
except Exception as e:
    print(f"Failed to load STL file: {e}")
