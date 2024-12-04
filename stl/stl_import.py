from tkinter import filedialog, messagebox
import pyvista as pv
from PIL import Image, ImageTk

def load_and_display_stl(app):
    """Load and display an STL file."""
    file_path = filedialog.askopenfilename(
        title="Select an STL File", filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
    )

    if not file_path:
        return  # User canceled

    try:
        app.log_message(f"Loading STL file: {file_path}")
        mesh = pv.read(file_path)
        write_path(file_path)

        # Display STL file in PyVista plotter
        plotter = pv.Plotter(window_size=(600, 400), off_screen=True)
        plotter.add_mesh(mesh, color="lightblue")
        plotter.add_axes()
        plotter.view_isometric()

        # Display in the canvas
        img = plotter.screenshot()
        display_image_in_canvas(app, img)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load STL file:\n{e}")


def display_image_in_canvas(app, img):
    """Display an image in the Tkinter canvas."""
    img = Image.fromarray(img)
    app.canvas_image = ImageTk.PhotoImage(img)
    app.stl_canvas.create_image(0, 0, anchor="nw", image=app.canvas_image)


def write_path(file_path):
    f = open("stl/stl_path.txt", "w")
    f.write(file_path)
    f.close()
