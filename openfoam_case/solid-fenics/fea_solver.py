from fenics import *
import numpy as np

# Load the mesh from a file
def load_mesh(mesh_file):
    mesh = Mesh()
    with XDMFFile(mesh_file) as xdmf:
        xdmf.read(mesh)
    return mesh

# Define material properties
E = 1e5  # Young's modulus (Pa)
nu = 0.3  # Poisson's ratio
mu = E / (2 * (1 + nu))  # Shear modulus
lambda_ = E * nu / ((1 + nu) * (1 - 2 * nu))  # Lame's first parameter

# Define the problem domain
mesh_file = "your_mesh.xdmf"  # Replace with your mesh file
mesh = load_mesh(mesh_file)

# Define function space
V = VectorFunctionSpace(mesh, "Lagrange", degree=1)

# Boundary condition
tol = 1e-14
clamped_boundary = lambda x, on_boundary: on_boundary and near(x[1], 0, tol)
bc = DirichletBC(V, Constant((0, 0)), clamped_boundary)

# Define strain and stress
def epsilon(u):
    return sym(grad(u))

def sigma(u):
    return lambda_ * div(u) * Identity(2) + 2 * mu * epsilon(u)

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant((0, -1000))  # Body force, e.g., gravity
a = inner(sigma(u), epsilon(v)) * dx
L = dot(f, v) * dx

# Solve the problem
u_solution = Function(V)
solve(a == L, u_solution, bc)

# Save solution to file for visualization
output_file = XDMFFile("output/fea_solution.xdmf")
output_file.write(u_solution)

print("FEA simulation complete!")

