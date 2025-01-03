import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from stl.stl_import import load_and_display_stl
from mesh.mesh_creation import generate_mesh
from mesh.blockmesh_generation import BlockMeshGenerator
from solve.define_params import DefineParams
from solve.run_solvers import run_solvers


class MeshGenerationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STL Viewer and Mesh Generator")

        # Configure the main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add STL Viewer tab
        self.stl_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stl_tab, text="STL Viewer")
        self.setup_stl_tab()

        # Add Mesh Generation tab
        self.block_mesh_generator = BlockMeshGenerator()
        self.mesh_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.mesh_tab, text="Mesh Generator")
        self.setup_mesh_tab()

        # BlockMesh generator instance
        #self.block_mesh_generator = BlockMeshGenerator()

        # Add CFD Solver 
        self.cfd_solve_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cfd_solve_tab, text="CFD Solver")
        self.setup_cfd_solve_tab()

        self.params_gen = DefineParams()

        # Add FEA Solver
        self.fea_solve_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fea_solve_tab, text="FEA Solver")
        self.setup_fea_solve_tab()

        # Add Coupled Solver
        self.coupled_solve_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.coupled_solve_tab, text="Coupled Solver")
        self.setup_coupled_solve_tab()

    def setup_stl_tab(self):
        """Set up the STL Viewer tab."""
        self.stl_canvas = tk.Canvas(self.stl_tab, bg="white", width=600, height=400)
        self.stl_canvas.pack(fill=tk.BOTH, expand=True)

        self.load_stl_button = ttk.Button(
            self.stl_tab, text="Load STL File", command=lambda: load_and_display_stl(self)
        )
        self.load_stl_button.pack(pady=10)

    def setup_mesh_tab(self):
        """Set up the Mesh Generation tab."""
        f = open("stl/stl_path.txt")

        try:
            self.generate_mesh_button = ttk.Button(
                self.mesh_tab,
                text="Generate OpenFOAM Mesh (snappyHexMesh)",
                command=lambda: generate_mesh(self, f.read()),
            )
            self.generate_mesh_button.pack(pady=10)
        except Exception as e:
            print("STL Path: " + f.read())
            messagebox.showerror("Error", f"Failed to generate mesh:\n{e}.")

        # Add BlockMesh functionality
        self.block_mesh_button = ttk.Button(
            self.mesh_tab,
            text="Generate OpenFOAM Mesh (blockMesh)",
            command=self.configure_and_generate_blockmesh,
        )
        self.block_mesh_button.pack(pady=10)

        self.visualize_button = ttk.Button(
            self.mesh_tab,
            text="Visualize Mesh and STL",
            command=lambda: self.block_mesh_generator.visualize_mesh(f.read()),
            #command=self.visualize_mesh_and_stl,
        )
        self.visualize_button.pack(pady=10)

        # Log area for messages
        self.log_frame = ttk.Frame(self.mesh_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """Log a message in the GUI."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def setup_cfd_solve_tab(self):
        """setup solve tab"""
        self.params_button = ttk.Button(
            self.cfd_solve_tab,
            text="Generate Param Files for pimpleFoam Solver",
            command=lambda: self.configure_params('cfd'),
        )
        self.params_button.pack(pady=10)

        self.cfd_solve_button = ttk.Button(
            self.cfd_solve_tab,
            text="Run pimpleFoam Solver",
            command=lambda: run_solvers('cfd')
        )
        self.cfd_solve_button.pack(pady=10)

        # Log area for messages
        self.log_frame = ttk.Frame(self.cfd_solve_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def setup_fea_solve_tab(self):
        """setup solve tab"""
        self.params_button = ttk.Button(
            self.fea_solve_tab,
            text="Generate Param Files for solids4Foam Solver",
            command=lambda: self.configure_params('fea'),
        )
        self.params_button.pack(pady=10)

        self.fea_solve_button = ttk.Button(
            self.fea_solve_tab,
            text="Run solids4Foam Solver",
            command=lambda: run_solvers('fea')
        )
        self.fea_solve_button.pack(pady=10)

        # Log area for messages
        self.log_frame = ttk.Frame(self.fea_solve_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)


    def setup_coupled_solve_tab(self):
        """setup solve tab"""
        self.params_button = ttk.Button(
            self.coupled_solve_tab,
            text="Generate Param Files for pimpleFoam and solids4Foam Solver",
            command=lambda: self.configure_params('coupled'),
        )
        self.params_button.pack(pady=10)

        self.coupled_solve_button = ttk.Button(
            self.coupled_solve_tab,
            text="Run pimpleFoam and solids4Foam Solvers",
            command=lambda: run_solvers('coupled')
        )
        self.coupled_solve_button.pack(pady=10)

        # Log area for messages
        self.log_frame = ttk.Frame(self.coupled_solve_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def configure_params(self, operation):
        """Open pop-up..."""
        def on_submit():
            try:
                if operation=='cfd':
                    # Get values from the fields
                    velocity_dimensions = velocity_dimensions.get("1.0", tk.END).strip()
                    velocity_if = velocity_if.get("1.0", tk.END).strip()
                    velocity_bf = velocity_bf.get("1.0", tk.END).strip()
                    pressure_dimensions = pressure_dimensions.get("1.0", tk.END).strip()
                    pressure_if = pressure_if.get("1.0", tk.END).strip()
                    pressure_bf = pressure_bf.get("1.0", tk.END).strip()

                    # Write parameter files
                    self.params_gen.write_vel_params(
                        dimensions=velocity_dimensions,
                        internalField=velocity_if,
                        boundaryField=velocity_bf
                    )

                    self.params_gen.write_pres_params(
                        dimensions=pressure_dimensions,
                        internalField=pressure_if,
                        boundaryField=pressure_bf
                    )
                    
                    self.log_message("U and P Parameter generation completed successfully.")
                    popup.destroy()
                
                elif operation=='fea':
                    # Get values from the fields
                    solidd_dimensions = solidd_dimensions.get("1.0", tk.END).strip()
                    solidd_if = solidd_if.get("1.0", tk.END).strip()
                    solidd_bf = solidd_bf.get("1.0", tk.END).strip()
                    nodald_dimensions = nodald_dimensions.get("1.0", tk.END).strip()
                    nodald_if = nodald_if.get("1.0", tk.END).strip()
                    nodald_bf = nodald_bf.get("1.0", tk.END).strip()
                    solidf_dimensions = solidf_dimensions.get("1.0", tk.END).strip()
                    solidf_if = solidf_if.get("1.0", tk.END).strip()
                    solidf_bf = solidf_bf.get("1.0", tk.END).strip()

                    # Write parameter files
                    self.params_gen.write_soliddef_params(
                        dimensions=solidd_dimensions,
                        internalField=solidd_if,
                        boundaryField=solidd_bf
                    )

                    self.params_gen.write_nodaldis_params(
                        dimensions=nodald_dimensions,
                        internalField=nodald_if,
                        boundaryField=nodald_bf
                    )

                    self.params_gen.write_solidfor_params(
                        dimensions=solidf_dimensions,
                        internalField=solidf_if,
                        boundaryField=solidf_bf
                    )
                    
                    self.log_message("U, P, D, pointD, solidForce Parameter generation completed successfully.")
                    popup.destroy()

                else:
                    # Get values from the fields
                    velocity_dimensions = velocity_dimensions.get("1.0", tk.END).strip()
                    velocity_if = velocity_if.get("1.0", tk.END).strip()
                    velocity_bf = velocity_bf.get("1.0", tk.END).strip()
                    pressure_dimensions = pressure_dimensions.get("1.0", tk.END).strip()
                    pressure_if = pressure_if.get("1.0", tk.END).strip()
                    pressure_bf = pressure_bf.get("1.0", tk.END).strip()
                    solidd_dimensions = solidd_dimensions.get("1.0", tk.END).strip()
                    solidd_if = solidd_if.get("1.0", tk.END).strip()
                    solidd_bf = solidd_bf.get("1.0", tk.END).strip()
                    nodald_dimensions = nodald_dimensions.get("1.0", tk.END).strip()
                    nodald_if = nodald_if.get("1.0", tk.END).strip()
                    nodald_bf = nodald_bf.get("1.0", tk.END).strip()
                    solidf_dimensions = solidf_dimensions.get("1.0", tk.END).strip()
                    solidf_if = solidf_if.get("1.0", tk.END).strip()
                    solidf_bf = solidf_bf.get("1.0", tk.END).strip()

                    # Write parameter files
                    self.params_gen.write_vel_params(
                        dimensions=velocity_dimensions,
                        internalField=velocity_if,
                        boundaryField=velocity_bf
                    )

                    self.params_gen.write_pres_params(
                        dimensions=pressure_dimensions,
                        internalField=pressure_if,
                        boundaryField=pressure_bf
                    )

                    self.params_gen.write_soliddef_params(
                        dimensions=solidd_dimensions,
                        internalField=solidd_if,
                        boundaryField=solidd_bf
                    )

                    self.params_gen.write_nodaldis_params(
                        dimensions=nodald_dimensions,
                        internalField=nodald_if,
                        boundaryField=nodald_bf
                    )

                    self.params_gen.write_solidfor_params(
                        dimensions=solidf_dimensions,
                        internalField=solidf_if,
                        boundaryField=solidf_bf
                    )

                    self.log_message("D, pointD, solidForce Parameter generation completed successfully.")
                    popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        
        popup = tk.Toplevel(self.root)
        popup.title("Configure Solver Parameters")
        popup.geometry("600x400")
        
        if operation=='cfd':
            ttk.Label(popup, text="Velocity Dimensions:").pack(anchor="w", padx=10)
            velocity_dimensions = tk.Text(popup, height=5, width=70)
            velocity_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Velocity Internal Field:").pack(anchor="w", padx=10)
            velocity_if = tk.Text(popup, height=5, width=70)
            velocity_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Velocity Boundary Field:").pack(anchor="w", padx=10)
            velocity_bf = tk.Text(popup, height=5, width=70)
            velocity_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Dimensions:").pack(anchor="w", padx=10)
            pressure_dimensions = tk.Text(popup, height=5, width=70)
            pressure_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Internal Field:").pack(anchor="w", padx=10)
            pressure_if = tk.Text(popup, height=5, width=70)
            pressure_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Boundary Field:").pack(anchor="w", padx=10)
            pressure_bf = tk.Text(popup, height=5, width=70)
            pressure_bf.pack(padx=10, pady=5)

            ttk.Button(popup, text="Submit", command=on_submit).pack(pady=10)

            popup.transient(self.root)  # Make the window modal
            popup.grab_set()
            self.root.wait_window(popup)
        
        elif operation=='fea':
            ttk.Label(popup, text="Solid Deformation Dimensions:").pack(anchor="w", padx=10)
            solidd_dimensions = tk.Text(popup, height=5, width=70)
            solidd_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Deformation Internal Field:").pack(anchor="w", padx=10)
            solidd_if = tk.Text(popup, height=5, width=70)
            solidd_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Deformation Boundary Field:").pack(anchor="w", padx=10)
            solidd_bf = tk.Text(popup, height=5, width=70)
            solidd_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Dimensions:").pack(anchor="w", padx=10)
            nodald_dimensions = tk.Text(popup, height=5, width=70)
            nodald_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Internal Field:").pack(anchor="w", padx=10)
            nodald_if = tk.Text(popup, height=5, width=70)
            nodald_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Boundary Field:").pack(anchor="w", padx=10)
            nodald_bf = tk.Text(popup, height=5, width=70)
            nodald_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Dimensions:").pack(anchor="w", padx=10)
            solidf_dimensions = tk.Text(popup, height=5, width=70)
            solidf_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Internal Field:").pack(anchor="w", padx=10)
            solidf_if = tk.Text(popup, height=5, width=70)
            solidf_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Boundary Field:").pack(anchor="w", padx=10)
            solidf_bf = tk.Text(popup, height=5, width=70)
            solidf_bf.pack(padx=10, pady=5)

            ttk.Button(popup, text="Submit", command=on_submit).pack(pady=10)

            popup.transient(self.root)  # Make the window modal
            popup.grab_set()
            self.root.wait_window(popup)
        
        else:
            ttk.Label(popup, text="Velocity Dimensions:").pack(anchor="w", padx=10)
            velocity_dimensions = tk.Text(popup, height=5, width=70)
            velocity_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Velocity Internal Field:").pack(anchor="w", padx=10)
            velocity_if = tk.Text(popup, height=5, width=70)
            velocity_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Velocity Boundary Field:").pack(anchor="w", padx=10)
            velocity_bf = tk.Text(popup, height=5, width=70)
            velocity_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Dimensions:").pack(anchor="w", padx=10)
            pressure_dimensions = tk.Text(popup, height=5, width=70)
            pressure_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Internal Field:").pack(anchor="w", padx=10)
            pressure_if = tk.Text(popup, height=5, width=70)
            pressure_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Pressure Boundary Field:").pack(anchor="w", padx=10)
            pressure_bf = tk.Text(popup, height=5, width=70)
            pressure_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Deformation Dimensions:").pack(anchor="w", padx=10)
            solidd_dimensions = tk.Text(popup, height=5, width=70)
            solidd_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Deformation Internal Field:").pack(anchor="w", padx=10)
            solidd_if = tk.Text(popup, height=5, width=70)
            solidd_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Deformation Boundary Field:").pack(anchor="w", padx=10)
            solidd_bf = tk.Text(popup, height=5, width=70)
            solidd_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Dimensions:").pack(anchor="w", padx=10)
            nodald_dimensions = tk.Text(popup, height=5, width=70)
            nodald_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Internal Field:").pack(anchor="w", padx=10)
            nodald_if = tk.Text(popup, height=5, width=70)
            nodald_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Nodal Displacement Boundary Field:").pack(anchor="w", padx=10)
            nodald_bf = tk.Text(popup, height=5, width=70)
            nodald_bf.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Dimensions:").pack(anchor="w", padx=10)
            solidf_dimensions = tk.Text(popup, height=5, width=70)
            solidf_dimensions.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Internal Field:").pack(anchor="w", padx=10)
            solidf_if = tk.Text(popup, height=5, width=70)
            solidf_if.pack(padx=10, pady=5)

            ttk.Label(popup, text="Solid Force Boundary Field:").pack(anchor="w", padx=10)
            solidf_bf = tk.Text(popup, height=5, width=70)
            solidf_bf.pack(padx=10, pady=5)

            ttk.Button(popup, text="Submit", command=on_submit).pack(pady=10)

            popup.transient(self.root)  # Make the window modal
            popup.grab_set()
            self.root.wait_window(popup)


    
    def configure_and_generate_blockmesh(self):
        """Open a pop-up window for BlockMesh configuration and run the mesh generator."""
        def on_submit():
            try:
                # Get values from the fields
                vertices = vertices_field.get("1.0", tk.END).strip()
                blocks = blocks_field.get("1.0", tk.END).strip()
                edges = edges_field.get("1.0", tk.END).strip()
                boundary = boundary_field.get("1.0", tk.END).strip()
                merge_patch_pairs = mpp_field.get("1.0", tk.END).strip()

                # Update the BlockMesh dictionary
                #self.block_mesh_generator.vertices = vertices
                #self.block_mesh_generator.blocks = blocks
                #self.block_mesh_generator.boundary = boundary

                # Write and generate mesh
                self.block_mesh_generator.write_block_mesh_dict(
                    vertices=vertices,
                    blocks=blocks,
                    edges=edges,
                    boundary=boundary,
                    merge_patch_pairs=merge_patch_pairs
                )
                self.block_mesh_generator.run_block_mesh()
                self.log_message("BlockMesh generation completed successfully.")
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Pop-up window for BlockMesh configuration
        popup = tk.Toplevel(self.root)
        popup.title("Configure BlockMesh Parameters")
        popup.geometry("600x400")

        ttk.Label(popup, text="Vertices (e.g., (0 0 0) ...):").pack(anchor="w", padx=10)
        vertices_field = tk.Text(popup, height=5, width=70)
        vertices_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Blocks (e.g., hex ...):").pack(anchor="w", padx=10)
        blocks_field = tk.Text(popup, height=5, width=70)
        blocks_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Edges (e.g., arc ...):").pack(anchor="w", padx=10)
        edges_field = tk.Text(popup, height=5, width=70)
        edges_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Boundary conditions:").pack(anchor="w", padx=10)
        boundary_field = tk.Text(popup, height=5, width=70)
        boundary_field.pack(padx=10, pady=5)

        ttk.Label(popup, text="Merge Patch Pairs:").pack(anchor="w", padx=10)
        mpp_field = tk.Text(popup, height=5, width=70)
        mpp_field.pack(padx=10, pady=5)

        ttk.Button(popup, text="Submit", command=on_submit).pack(pady=10)

        popup.transient(self.root)  # Make the window modal
        popup.grab_set()
        self.root.wait_window(popup)


if __name__ == "__main__":
    root = tk.Tk()
    app = MeshGenerationApp(root)
    root.geometry("800x600")
    root.mainloop()
