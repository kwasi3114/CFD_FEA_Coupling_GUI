from fenics import *
from fenicsprecice import Adapter
import meshio
import numpy as np

# Load the mesh from a .vtu/.vtp file
def load_mesh(mesh_file):
    mesh = Mesh()
    with XDMFFile(mesh_file) as xdmf:
        xdmf.read(mesh)
    return mesh

# Define material properties and constants
E = 1e5  # Young's modulus
nu = 0.3  # Poisson's ratio
rho = 1e3  # Density
mu = E / (2 * (1 + nu))
lambda_ = E * nu / ((1 + nu) * (1 - 2 * nu))

# Load OpenFOAM mesh
mesh_file = "/home/kwasi_dp/CFD_FEA_Coupling_GUI/stl/tesla_translated.xdmf"
mesh = load_mesh(mesh_file)

# Define function space
V = VectorFunctionSpace(mesh, "Lagrange", degree=1)

# Define trial, test, and function spaces
u = TrialFunction(V)
v = TestFunction(V)
u_n = Function(V)
u_np1 = Function(V)

# Boundary conditions
tol = 1e-14
clamped_boundary = lambda x, on_boundary: on_boundary and near(x[1], 0, tol)
bc = DirichletBC(V, Constant((0, 0)), clamped_boundary)

# Define strain and stress
def epsilon(u):
    return sym(grad(u))

def sigma(u):
    return lambda_ * div(u) * Identity(3) + 2 * mu * epsilon(u)

# Coupling setup with preCICE
precice = Adapter(adapter_config_filename="precice-adapter-config-fsi.json")
coupling_boundary = MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
coupling_boundary.set_all(0)

# Tag coupling boundary using a custom condition
for f in facets(mesh):
    if f.exterior() and near(f.midpoint().y(), 1.0, tol):
        coupling_boundary[f.index()] = 1

precice.initialize(
    coupling_boundary=coupling_boundary,
    read_function_space=V,
    write_object=V,
)

# Time-stepping parameters
dt = Constant(precice.get_max_time_step_size())
t = 0.0
T = 1.0  # Simulation end time
gamma = 0.5
beta = 0.25

# Variational form
a_form = rho * inner(u, v) * dx + dt ** 2 * inner(sigma(u), grad(v)) * dx
L_form = rho * inner(u_n, v) * dx

# Prepare output
output = XDMFFile("output/fsi_solution.xdmf")
output.parameters["flush_output"] = True

# Time-stepping loop
while precice.is_coupling_ongoing() and t < T:
    # Read data from preCICE
    precice.read_data(u_np1)

    # Solve FEA problem
    A, b = assemble_system(a_form, L_form, bc)
    solve(A, u_np1.vector(), b)

    # Write data to preCICE
    precice.write_data(u_np1)

    # Advance coupling
    precice.advance(float(dt))

    # Update solution
    u_n.assign(u_np1)

    # Save solution to output
    output.write(u_np1, t)

    # Advance time
    t += float(dt)

# Finalize coupling
precice.finalize()

print("Simulation complete!")

