import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from io_utils import read_points
from voronoi_engine import compute_voronoi, plot_voronoi_colored
from exporter import export_diagram


class VoronoiApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Voronoi Generator")

        self.canvas = None
        self.voronoi = None

        tk.Button(root, text="Load points", command=self.load).pack(pady=5)
        tk.Button(root, text="Export", command=self.export).pack(pady=5)

    def load(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            pts = read_points(path)
            self.voronoi = compute_voronoi(pts)
            self.display()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display(self):
        fig = plot_voronoi_colored(self.voronoi)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def export(self):
        if self.voronoi is None:
            messagebox.showwarning("Warning", "Load points first")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("SVG", "*.svg"),
                ("JPG", "*.jpg"),
            ],
        )

        if filename:
            export_diagram(self.voronoi, filename)