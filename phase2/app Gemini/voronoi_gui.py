import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from scipy.spatial import Voronoi
from voronoi_core import load_points_from_file, compute_voronoi

class VoronoiApp:
    """Application graphique pour visualiser les diagrammes de Voronoï."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Générateur de Diagrammes de Voronoï")
        self.root.geometry("800x600")

        self.points = None
        self.voronoi = None

        self._setup_ui()

    def _setup_ui(self):
        """Initialise les composants de l'interface utilisateur."""
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X)

        btn_load = tk.Button(control_frame, text="Charger des points (CSV/TXT)", command=self.load_file)
        btn_load.pack(side=tk.LEFT, padx=10)

        btn_export_png = tk.Button(control_frame, text="Exporter en PNG/JPG", command=lambda: self.export_plot('png'))
        btn_export_png.pack(side=tk.LEFT, padx=5)

        btn_export_svg = tk.Button(control_frame, text="Exporter en SVG", command=lambda: self.export_plot('svg'))
        btn_export_svg.pack(side=tk.LEFT, padx=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

        self._draw_empty_state()

    def _draw_empty_state(self):
        """Affiche un message par défaut avant le chargement des données."""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Veuillez charger un fichier de points",
                     horizontalalignment='center', verticalalignment='center',
                     transform=self.ax.transAxes, color="gray")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def load_file(self):
        """Ouvre une boîte de dialogue pour charger le fichier et met à jour l'affichage."""
        filepath = filedialog.askopenfilename(
            title="Sélectionner un fichier",
            filetypes=(("Fichiers texte", "*.txt;*.csv"), ("Tous les fichiers", "*.*"))
        )

        if not filepath:
            return

        try:
            self.points = load_points_from_file(filepath)
            self.voronoi, error_msg = compute_voronoi(self.points)

            if self.voronoi is None:
                messagebox.showerror("Erreur de calcul", error_msg)
                return

            self.update_plot()

        except ValueError as e:
            messagebox.showerror("Erreur de lecture", str(e))

    def update_plot(self):
        """Met à jour le canevas avec le diagramme de Voronoï coloré."""
        self.ax.clear()
        if self.voronoi:
            points = self.points

            # 1. Calcul de la boîte englobante pour cadrer l'affichage
            min_x, max_x = points[:, 0].min(), points[:, 0].max()
            min_y, max_y = points[:, 1].min(), points[:, 1].max()
            dx, dy = max_x - min_x, max_y - min_y
            cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2

            # 2. Astuce des "points fantômes" pour fermer les régions infinies
            radius = max(dx, dy) * 10 if max(dx, dy) > 0 else 10
            dummy_points = np.array([
                [cx - radius, cy - radius], [cx + radius, cy - radius],
                [cx + radius, cy + radius], [cx - radius, cy + radius]
            ])
            all_points = np.vstack((points, dummy_points))
            vor_display = Voronoi(all_points)

            # 3. Génération d'une palette de couleurs agréables
            cmap = plt.get_cmap('tab20')
            np.random.seed(42) # Pour que les couleurs restent les mêmes au rechargement
            colors = cmap(np.linspace(0, 1, len(points)))
            np.random.shuffle(colors)

            # 4. Dessin et remplissage des polygones
            for i, region_idx in enumerate(vor_display.point_region[:len(points)]):
                region = vor_display.regions[region_idx]
                if -1 not in region and len(region) > 0:
                    polygon = [vor_display.vertices[v] for v in region]
                    x, y = zip(*polygon)
                    # On colorie l'intérieur et on dessine des bordures blanches
                    self.ax.fill(x, y, color=colors[i], alpha=0.7, edgecolor='white', linewidth=1.5)

            # 5. Affichage des points d'origine
            self.ax.plot(points[:, 0], points[:, 1], 'ko', markersize=5, zorder=3)

            # 6. Restreindre la vue pour cacher les points fantômes
            margin_x = dx * 0.1 if dx > 0 else 1
            margin_y = dy * 0.1 if dy > 0 else 1
            self.ax.set_xlim(min_x - margin_x, max_x + margin_x)
            self.ax.set_ylim(min_y - margin_y, max_y + margin_y)

            self.ax.set_title("Diagramme de Voronoï")
            self.canvas.draw()

    def export_plot(self, fmt: str):
        """Exporte le diagramme actuellement affiché."""
        if self.voronoi is None:
            messagebox.showwarning("Avertissement", "Aucun diagramme à exporter.")
            return

        filetypes = [("Fichier SVG", "*.svg")] if fmt == 'svg' else [("Images", "*.png;*.jpg;*.jpeg")]
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{fmt}", filetypes=filetypes, title=f"Enregistrer en tant que {fmt.upper()}"
        )

        if filepath:
            try:
                self.fig.savefig(filepath, format=fmt, bbox_inches='tight', dpi=300)
                messagebox.showinfo("Succès", f"Fichier sauvegardé avec succès :\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur d'exportation", f"Impossible de sauvegarder le fichier : {e}")