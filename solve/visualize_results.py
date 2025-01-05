import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from tkinter import Tk, Checkbutton, IntVar, Button, Label, Frame

# Sample data for solver results (replace with actual solver outputs)
time = np.linspace(0, 10, 100)  # Time variable
solver1_results = {
    "Displacement": np.sin(time),
    "Velocity": np.cos(time),
    "Acceleration": -np.sin(time),
}
solver2_results = {
    "Displacement": np.sin(time) + 0.1,
    "Velocity": np.cos(time) - 0.1,
    "Acceleration": -np.sin(time) + 0.1,
}

# Sample meshes over time (replace these with your actual meshes)
mesh1 = pv.Sphere(radius=1)
mesh2 = pv.Sphere(radius=1.1)

solver1_meshes = [mesh1.scale((1 + t/20, 1 + t/20, 1 + t/20)) for t in time]
solver2_meshes = [mesh2.scale((1 - t/30, 1 - t/30, 1 - t/30)) for t in time]

# GUI for parameter and mesh selection
class SolverVisualizer:
    def __init__(self, root, parameters, plot_callback, mesh_callback):
        self.root = root
        self.parameters = parameters
        self.plot_callback = plot_callback
        self.mesh_callback = mesh_callback
        self.variables = {param: IntVar(value=1) for param in parameters}

        self.frame = Frame(root)
        self.frame.pack()

        Label(self.frame, text="Select Parameters to Plot:").pack(anchor="w")
        for param in self.parameters:
            Checkbutton(self.frame, text=param, variable=self.variables[param], command=self.update_plot).pack(anchor="w")

        Button(self.frame, text="Visualize Mesh", command=self.update_mesh).pack()
        Button(self.frame, text="Exit", command=self.root.destroy).pack()

    def update_plot(self):
        selected_params = [param for param, var in self.variables.items() if var.get()]
        self.plot_callback(selected_params)

    def update_mesh(self):
        self.mesh_callback()

# Function to plot results
def plot_results(selected_params):
    plt.clf()  # Clear the current plot
    for param in selected_params:
        plt.plot(time, solver1_results[param], label=f"Solver 1: {param}")
        plt.plot(time, solver2_results[param], '--', label=f"Solver 2: {param}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Solver Results Comparison")
    plt.legend()
    plt.grid(True)
    plt.pause(0.1)  # Update the plot interactively

# Function to visualize meshes
def visualize_meshes():
    # Create PyVista plotter
    plotter = pv.Plotter(shape=(1, 2))

    # Add initial meshes
    plotter.subplot(0, 0)
    plotter.add_mesh(solver1_meshes[0], color="blue", opacity=0.7)
    plotter.add_text("Solver 1 Mesh", font_size=12)

    plotter.subplot(0, 1)
    plotter.add_mesh(solver2_meshes[0], color="red", opacity=0.7)
    plotter.add_text("Solver 2 Mesh", font_size=12)

    def update_mesh(frame):
        plotter.subplot(0, 0)
        plotter.clear()
        plotter.add_mesh(solver1_meshes[frame], color="blue", opacity=0.7)
        plotter.add_text("Solver 1 Mesh", font_size=12)

        plotter.subplot(0, 1)
        plotter.clear()
        plotter.add_mesh(solver2_meshes[frame], color="red", opacity=0.7)
        plotter.add_text("Solver 2 Mesh", font_size=12)

    # Animate over time
    for t in range(len(time)):
        update_mesh(t)
        plotter.update()
        plotter.sleep(0.1)

    plotter.show()

# Main function
def main():
    root = Tk()
    root.title("Solver Results and Mesh Visualization")

    # Initialize plot
    plt.ion()  # Enable interactive mode
    plt.figure()
    plt.show()

    # Start GUI
    parameters = list(solver1_results.keys())
    visualizer = SolverVisualizer(root, parameters, plot_results, visualize_meshes)

    # Start Tkinter main loop
    root.mainloop()
    plt.ioff()  # Disable interactive mode
    plt.show()  # Keep the final plot open

if __name__ == "__main__":
    main()

