import pyvista as pv
import os

def visualize_mesh_and_stl(stl_path, vtk_mesh_path):
    """
    Visualize the STL file and the generated mesh in the same PyVista plot.

    Parameters:
    stl_path (str): Path to the STL file.
    vtk_mesh_path (str): Path to the VTK file representing the mesh.
    """
    try:
        # Load the STL file
        stl_mesh = pv.read(stl_path)

        # Load the mesh from the VTK file
        if not os.path.exists(vtk_mesh_path):
            print(f"Mesh file not found: {vtk_mesh_path}")
            return

        foam_mesh = pv.read(vtk_mesh_path)

        # Create a PyVista plotter
        plotter = pv.Plotter()

        stl_bounds = stl_mesh.bounds
        foam_bounds = foam_mesh.bounds

        # Calculate STL and foam mesh centers
        stl_center = [(stl_bounds[1] + stl_bounds[0]) / 2,
                      (stl_bounds[3] + stl_bounds[2]) / 2,
                      (stl_bounds[5] + stl_bounds[4]) / 2]

        foam_center = [(foam_bounds[1] + foam_bounds[0]) / 2,
                       (foam_bounds[3] + foam_bounds[2]) / 2,
                       (foam_bounds[5] + foam_bounds[4]) / 2]
        
        print("STL Center: " + str(stl_center))
        print("BlockMesh Center: " + str(foam_center))
        trans = stl_mesh.translate((-1103.1154174804688, -738.1376037597656, -2315.1011962890625), inplace=False)

        # Add the STL geometry to the plot
        #plotter.add_mesh(stl_mesh, color="gray", opacity=0.5, label="STL Geometry")
        plotter.add_mesh(trans, color="gray", opacity=0.5, label="STL Geometry")

        # Add the generated mesh to the plot
        plotter.add_mesh(
            foam_mesh,
            color="lightblue",
            opacity=0.7,
            show_edges=True,
            edge_color="blue",
            label="Generated Mesh",
        )

        # Add a legend and display the plot
        plotter.add_legend()
        plotter.show()

    except Exception as e:
        print(f"An error occurred while visualizing: {e}")

# Example usage
if __name__ == "__main__":
    stl_path = "/home/kwasi_dp/CFD_FEA_Coupling_GUI/stl/tesla.stl"  # Replace with the actual STL file path
    vtk_mesh_path = "/home/kwasi_dp/CFD_FEA_Coupling_GUI/openfoam_case/VTK/openfoam_case_0.vtm"  # Replace with the actual VTK mesh file path
    #print("Aligned STL Bounds:", stl_mesh.bounds)
    #print("Aligned Foam Mesh Bounds:", foam_mesh.bounds)


    visualize_mesh_and_stl(stl_path, vtk_mesh_path)

    

