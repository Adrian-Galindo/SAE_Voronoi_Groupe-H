"""Widget de visualisation Matplotlib intégré dans Tkinter."""
# pylint: disable=wrong-import-position,wrong-import-order
# matplotlib.use() DOIT être appelé avant tout import du backend.
# Cela impose un ordre d'import non standard — désactivation intentionnelle.
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon  # noqa: E402
from matplotlib import cm  # noqa: E402

# ── Constantes visuelles ──────────────────────────────────────────────────────
_COLOR_RIDGE = "#1a6faf"
_COLOR_SITE = "#c0392b"
_COLOR_VERTEX = "#27ae60"
_COLOR_PLACEHOLDER_BG = "#f0f4f8"

# Style global appliqué à toutes les figures de l'application
_MPL_RC = {
    "axes.facecolor": "#f8f9fa",
    "axes.edgecolor": "#ced4da",
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "font.family": "sans-serif",
    "legend.fontsize": 8,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "#ced4da",
}
matplotlib.rcParams.update(_MPL_RC)


# ── Options de rendu ──────────────────────────────────────────────────────────

@dataclass
class DrawOptions:
    """Paramètres de rendu transmis à la fonction de dessin."""
    show_points: bool = True
    show_vertices: bool = True
    show_labels: bool = True
    color_cells: bool = True


# ── Widget principal ──────────────────────────────────────────────────────────

class VoronoiCanvas(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Frame Tkinter contenant la figure Matplotlib et la barre de navigation."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._vor = None
        self._draw_opts = DrawOptions()   # nom distinct de _options() de tkinter
        self._build()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def _build(self) -> None:
        self.figure = Figure(figsize=(9, 7), dpi=100, facecolor="white")
        self.ax = self.figure.add_subplot(111)
        self._show_placeholder()

        self.mpl_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.nav_toolbar = NavigationToolbar2Tk(self.mpl_canvas, nav_frame)
        self.nav_toolbar.update()

        # Pan activé par défaut (glisser pour déplacer)
        self.nav_toolbar.pan()

        # Interactions souris personnalisées
        self.mpl_canvas.mpl_connect("scroll_event", self._on_scroll)
        self.mpl_canvas.mpl_connect("button_press_event", self._on_button_press)

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------

    def plot(self, vor, options: DrawOptions | None = None) -> None:
        """Dessine le diagramme de Voronoï. Sauvegarde les options pour redraw."""
        if options is not None:
            self._draw_opts = options
        self._vor = vor
        self.ax.clear()
        _draw_voronoi(vor, self.ax, self._draw_opts)
        self.mpl_canvas.draw()

    def redraw(self, options: DrawOptions) -> None:
        """Redessine avec de nouvelles options sans recharger les données."""
        if self._vor is not None:
            self.plot(self._vor, options)

    def reset_view(self) -> None:
        """Recentre la vue sur l'étendue initiale du diagramme."""
        self.nav_toolbar.home()

    def clear(self) -> None:
        """Réinitialise le canvas à son état vide."""
        self._vor = None
        self.ax.clear()
        self._show_placeholder()
        self.mpl_canvas.draw()

    def get_figure(self) -> Figure:
        """Retourne la figure Matplotlib (utilisé par les exporteurs)."""
        return self.figure

    # ------------------------------------------------------------------
    # Handlers souris
    # ------------------------------------------------------------------

    def _on_scroll(self, event) -> None:
        """Zoom centré sur le curseur avec la molette de la souris."""
        if event.inaxes is None:
            return
        ax = event.inaxes
        scale = 0.82 if event.button == "up" else 1.22
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        xc, yc = event.xdata, event.ydata
        ax.set_xlim(xc + (x_min - xc) * scale, xc + (x_max - xc) * scale)
        ax.set_ylim(yc + (y_min - yc) * scale, yc + (y_max - yc) * scale)
        self.mpl_canvas.draw_idle()

    def _on_button_press(self, event) -> None:
        """Double-clic gauche : réinitialise la vue."""
        if event.dblclick and event.button == 1:
            self.reset_view()

    # ------------------------------------------------------------------
    # Interne
    # ------------------------------------------------------------------

    def _show_placeholder(self) -> None:
        self.ax.set_facecolor(_COLOR_PLACEHOLDER_BG)
        self.ax.text(
            0.5, 0.5,
            "Ouvrez un fichier de points\npour afficher le diagramme de Voronoï",
            ha="center", va="center",
            transform=self.ax.transAxes,
            fontsize=13, color="#6c757d",
            bbox={
                "boxstyle": "round,pad=0.7",
                "facecolor": "white",
                "alpha": 0.92,
                "edgecolor": "#dee2e6",
            },
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)


# ── Fonctions de dessin (indépendantes du widget) ─────────────────────────────

def _draw_voronoi(vor, ax, options: DrawOptions) -> None:
    """Point d'entrée du rendu : délègue à des fonctions spécialisées."""
    x_min, x_max, y_min, y_max, extent = _compute_extent(vor.points)
    center = vor.points.mean(axis=0)

    if options.color_cells:
        _draw_cells(vor, ax)

    _draw_ridges(vor, ax, center, extent)

    if options.show_points:
        _draw_sites(vor.points, ax, options.show_labels)

    if options.show_vertices:
        _draw_voronoi_vertices(vor.vertices, ax)

    _style_axes(ax, x_min, x_max, y_min, y_max)


def _compute_extent(points: np.ndarray) -> tuple:
    """Calcule la fenêtre d'affichage avec marge autour des points."""
    span = max(float(np.ptp(points, axis=0).max()), 1.0)
    margin = 0.30 * span
    x_min = float(points[:, 0].min()) - margin
    x_max = float(points[:, 0].max()) + margin
    y_min = float(points[:, 1].min()) - margin
    y_max = float(points[:, 1].max()) + margin
    extent = max(x_max - x_min, y_max - y_min)
    return x_min, x_max, y_min, y_max, extent


def _draw_cells(vor, ax) -> None:
    """Colorie les cellules finies (sans bord infini) avec la palette Set3."""
    palette = cm.Set3(np.linspace(0, 1, max(len(vor.points), 1)))  # pylint: disable=no-member
    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        if not region or -1 in region:
            continue
        patch = MplPolygon(
            vor.vertices[region], closed=True,
            facecolor=palette[i % len(palette)],
            edgecolor="none", alpha=0.55, zorder=1,
        )
        ax.add_patch(patch)


def _draw_ridges(vor, ax, center: np.ndarray, extent: float) -> None:
    """Trace toutes les arêtes (finies en trait plein, semi-infinies en tirets)."""
    for (p1, p2), simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(
                vor.vertices[simplex, 0], vor.vertices[simplex, 1],
                color=_COLOR_RIDGE, lw=1.8, solid_capstyle="round", zorder=2,
            )
        else:
            # Arête semi-infinie : calcul du point lointain dans la bonne direction
            i = simplex[simplex >= 0][0]
            t = vor.points[p2] - vor.points[p1]
            norm = float(np.linalg.norm(t))
            if norm < 1e-12:
                continue
            t /= norm
            n = np.array([-t[1], t[0]])
            midpoint = (vor.points[p1] + vor.points[p2]) / 2.0
            sign = float(np.sign(np.dot(midpoint - center, n))) or 1.0
            far = vor.vertices[i] + sign * n * 2.0 * extent
            ax.plot(
                [vor.vertices[i, 0], far[0]], [vor.vertices[i, 1], far[1]],
                color=_COLOR_RIDGE, lw=1.8, ls="--", dash_capstyle="round", zorder=2,
            )


def _draw_sites(points: np.ndarray, ax, show_labels: bool) -> None:
    """Affiche les points d'entrée (sites) avec étiquettes optionnelles."""
    ax.scatter(
        points[:, 0], points[:, 1],
        s=65, c=_COLOR_SITE, edgecolors="white", linewidths=0.8,
        zorder=5, label="Sites",
    )
    if show_labels:
        for idx, pt in enumerate(points):
            ax.annotate(
                f" P{idx + 1}", xy=pt,
                fontsize=7.5, color="#2c3e50",
                fontweight="bold", zorder=6,
            )


def _draw_voronoi_vertices(vertices: np.ndarray, ax) -> None:
    """Affiche les sommets du diagramme de Voronoï."""
    if len(vertices) == 0:
        return
    ax.scatter(
        vertices[:, 0], vertices[:, 1],
        s=28, c=_COLOR_VERTEX, marker="^",
        edgecolors="white", linewidths=0.6,
        zorder=4, label="Sommets",
    )


def _style_axes(ax, x_min: float, x_max: float, y_min: float, y_max: float) -> None:
    """Applique le style final à l'axe (limites, grille, titres, légende)."""
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, color="#e0e0e0", linestyle="-", linewidth=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Diagramme de Voronoï", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="upper right", fancybox=True)
