"""Widget de visualisation Matplotlib intégré dans Tkinter."""
# pylint: disable=wrong-import-position,wrong-import-order
# matplotlib.use() doit être appelé avant tout import du backend,
# ce qui impose un ordre d'import non standard — désactivation intentionnelle.
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

_COULEUR_ARETE = "#1a6faf"
_COULEUR_SITE = "#c0392b"
_COULEUR_SOMMET = "#27ae60"
_COULEUR_FOND_VIDE = "#f0f4f8"

_STYLE_MPL = {
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
matplotlib.rcParams.update(_STYLE_MPL)


@dataclass
class DrawOptions:
    """Paramètres de rendu transmis à la fonction de dessin."""
    show_points: bool = True
    show_vertices: bool = False
    show_labels: bool = True
    color_cells: bool = True


class VoronoiCanvas(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Frame Tkinter contenant la figure Matplotlib et la barre de navigation."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._vor = None
        self._draw_opts = DrawOptions()
        self._construire_widget()

    # ── Construction ──────────────────────────────────────────────────────────

    def _construire_widget(self) -> None:
        self.figure = Figure(figsize=(9, 7), dpi=100, facecolor="white")
        self.ax = self.figure.add_subplot(111)
        self._afficher_ecran_vide()

        self.mpl_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.nav_toolbar = NavigationToolbar2Tk(self.mpl_canvas, nav_frame)
        self.nav_toolbar.update()
        self.nav_toolbar.pan()

        self.mpl_canvas.mpl_connect("scroll_event", self._sur_molette)
        self.mpl_canvas.mpl_connect("button_press_event", self._sur_clic_souris)

    # ── API publique ──────────────────────────────────────────────────────────

    def afficher_diagramme(self, vor, options: DrawOptions | None = None) -> None:
        """Dessine le diagramme de Voronoï et conserve les options pour un redessinage."""
        if options is not None:
            self._draw_opts = options
        self._vor = vor
        self.ax.clear()
        _tracer_diagramme_complet(vor, self.ax, self._draw_opts)
        self.mpl_canvas.draw()

    def redessiner(self, options: DrawOptions) -> None:
        """Applique de nouvelles options d'affichage sans recharger les données."""
        if self._vor is not None:
            self.afficher_diagramme(self._vor, options)

    def reinitialiser_vue(self) -> None:
        """Recentre la vue sur l'étendue initiale du diagramme."""
        self.nav_toolbar.home()

    def vider(self) -> None:
        """Réinitialise le canvas à son état vide (avant tout chargement)."""
        self._vor = None
        self.ax.clear()
        self._afficher_ecran_vide()
        self.mpl_canvas.draw()

    def obtenir_figure(self) -> Figure:
        """Retourne la figure Matplotlib utilisée par les exporteurs."""
        return self.figure

    # ── Événements souris ─────────────────────────────────────────────────────

    def _sur_molette(self, event) -> None:
        """Effectue un zoom centré sur la position du curseur."""
        if event.inaxes is None:
            return
        ax = event.inaxes
        echelle = 0.82 if event.button == "up" else 1.22
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        xc, yc = event.xdata, event.ydata
        ax.set_xlim(xc + (x_min - xc) * echelle, xc + (x_max - xc) * echelle)
        ax.set_ylim(yc + (y_min - yc) * echelle, yc + (y_max - yc) * echelle)
        self.mpl_canvas.draw_idle()

    def _sur_clic_souris(self, event) -> None:
        """Réinitialise la vue sur double-clic gauche."""
        if event.dblclick and event.button == 1:
            self.reinitialiser_vue()

    # ── Affichage interne ─────────────────────────────────────────────────────

    def _afficher_ecran_vide(self) -> None:
        self.ax.set_facecolor(_COULEUR_FOND_VIDE)
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


# ── Fonctions de dessin ───────────────────────────────────────────────────────

def _tracer_diagramme_complet(vor, ax, options: DrawOptions) -> None:
    """Orchestre le rendu complet du diagramme en appelant les sous-fonctions."""
    x_min, x_max, y_min, y_max, etendue = _calculer_etendue(vor.points)
    centre = vor.points.mean(axis=0)

    if options.color_cells:
        _colorier_cellules(vor, ax)

    _tracer_aretes(vor, ax, centre, etendue)

    if options.show_points:
        _tracer_sites(vor.points, ax, options.show_labels)

    if options.show_vertices:
        _tracer_sommets(vor.vertices, ax)

    _styler_axes(ax, x_min, x_max, y_min, y_max)


def _calculer_etendue(points: np.ndarray) -> tuple:
    """Calcule les limites d'affichage avec une marge proportionnelle à l'étendue."""
    ecart = max(float(np.ptp(points, axis=0).max()), 1.0)
    marge = 0.30 * ecart
    x_min = float(points[:, 0].min()) - marge
    x_max = float(points[:, 0].max()) + marge
    y_min = float(points[:, 1].min()) - marge
    y_max = float(points[:, 1].max()) + marge
    etendue = max(x_max - x_min, y_max - y_min)
    return x_min, x_max, y_min, y_max, etendue


def _colorier_cellules(vor, ax) -> None:
    """Colorie les cellules finies (sans arête infinie) avec la palette Set3."""
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


def _tracer_aretes(vor, ax, centre: np.ndarray, etendue: float) -> None:
    """Trace les arêtes finies en trait plein et les arêtes semi-infinies en tirets."""
    for (p1, p2), simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(
                vor.vertices[simplex, 0], vor.vertices[simplex, 1],
                color=_COULEUR_ARETE, lw=1.8, solid_capstyle="round", zorder=2,
            )
        else:
            # Direction perpendiculaire à la bissectrice des deux sites voisins
            i = simplex[simplex >= 0][0]
            t = vor.points[p2] - vor.points[p1]
            norme = float(np.linalg.norm(t))
            if norme < 1e-12:
                continue
            t /= norme
            n = np.array([-t[1], t[0]])
            milieu = (vor.points[p1] + vor.points[p2]) / 2.0
            signe = float(np.sign(np.dot(milieu - centre, n))) or 1.0
            lointain = vor.vertices[i] + signe * n * 2.0 * etendue
            ax.plot(
                [vor.vertices[i, 0], lointain[0]], [vor.vertices[i, 1], lointain[1]],
                color=_COULEUR_ARETE, lw=1.8, ls="--", dash_capstyle="round", zorder=2,
            )


def _tracer_sites(points: np.ndarray, ax, afficher_labels: bool) -> None:
    """Affiche les sites (points d'entrée) avec leurs étiquettes optionnelles."""
    ax.scatter(
        points[:, 0], points[:, 1],
        s=65, c=_COULEUR_SITE, edgecolors="white", linewidths=0.8,
        zorder=5, label="Sites",
    )
    if afficher_labels:
        for idx, pt in enumerate(points):
            ax.annotate(
                f" P{idx + 1}", xy=pt,
                fontsize=7.5, color="#2c3e50",
                fontweight="bold", zorder=6,
            )


def _tracer_sommets(sommets: np.ndarray, ax) -> None:
    """Affiche les sommets du diagramme de Voronoï sous forme de triangles."""
    if len(sommets) == 0:
        return
    ax.scatter(
        sommets[:, 0], sommets[:, 1],
        s=28, c=_COULEUR_SOMMET, marker="^",
        edgecolors="white", linewidths=0.6,
        zorder=4, label="Sommets",
    )


def _styler_axes(ax, x_min: float, x_max: float, y_min: float, y_max: float) -> None:
    """Applique les limites, la grille et les labels à l'axe."""
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, color="#e0e0e0", linestyle="-", linewidth=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Diagramme de Voronoï", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="upper right", fancybox=True)
