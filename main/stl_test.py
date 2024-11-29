import trimesh

file_path = r'C:\Users\kwasi\Downloads\stl_test.stl'

try:
    # Load the STL file
    mesh = trimesh.load(file_path)
    print("STL file loaded successfully!")
    print(mesh)
    
    # Visualize the mesh
    mesh.show()
except Exception as e:
    print(f"Failed to load STL file: {e}")
