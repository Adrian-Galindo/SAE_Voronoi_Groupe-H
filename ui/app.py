"""Fenêtre principale de l'application."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.parser import parse_points_file
from core.voronoi import compute_voronoi
from export.svg_exporter import export_svg
from export.image_exporter import export_image
from ui.canvas import VoronoiCanvas, DrawOptions
from ui.toolbar import Toolbar


class VoronoiApp(tk.Tk):  # pylint: disable=too-many-instance-attributes
    """Fenêtre principale : assemble la toolbar, le canvas, le panneau latéral
    et la barre de statut."""

    def __init__(self):
        super().__init__()
        self.title("Diagramme de Voronoï")
        self.geometry("1150x750")
        self.minsize(750, 500)

        self._vor = None
        self._points: list = []
        self._main_status = "Prêt  —  Ouvrez un fichier de points."

        # Variables du panneau latéral (affectées dans _build_side_panel)
        self.stat_points: tk.StringVar
        self.stat_vertices: tk.StringVar
        self.stat_regions: tk.StringVar
        self.opt_color: tk.BooleanVar
        self.opt_labels: tk.BooleanVar
        self.opt_vertices: tk.BooleanVar

        self._apply_theme()
        self._build_ui()

    # ------------------------------------------------------------------
    # Thème et construction de l'interface
    # ------------------------------------------------------------------

    def _apply_theme(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=(8, 4))
        style.configure("TLabelframe.Label", font=("Helvetica", 9, "bold"))
        style.configure("Hint.TLabel", foreground="#6c757d", font=("Helvetica", 8))

    def _build_ui(self) -> None:
        self._build_menu()

        callbacks = {
            "open": self._open_file,
            "export_svg": self._export_svg,
            "export_image": self._export_image,
            "reset_view": self._reset_view,
            "about": self._show_about,
        }
        self.toolbar = Toolbar(self, callbacks=callbacks)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)

        # Zone principale : canvas + panneau latéral
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas_widget = VoronoiCanvas(main_frame)
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self._build_side_panel(main_frame)

        # Barre de statut
        self.status_var = tk.StringVar(value=self._main_status)
        status_bar = ttk.Label(
            self, textvariable=self.status_var,
            relief=tk.SUNKEN, anchor=tk.W, padding=(8, 2),
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Coordonnées en temps réel dans la barre de statut
        self.canvas_widget.mpl_canvas.mpl_connect(
            "motion_notify_event", self._on_mouse_move
        )
        self.canvas_widget.mpl_canvas.mpl_connect(
            "axes_leave_event", self._on_axes_leave
        )

    def _build_side_panel(self, parent) -> None:
        """Construit le panneau latéral droit (stats + options + aide)."""
        panel = ttk.Frame(parent, width=195)
        panel.pack(fill=tk.Y, side=tk.RIGHT, padx=(6, 0))
        panel.pack_propagate(False)

        # ── Statistiques ──────────────────────────────────────────────
        stats_frame = ttk.LabelFrame(panel, text="Statistiques", padding=8)
        stats_frame.pack(fill=tk.X, pady=(0, 8))

        self.stat_points = tk.StringVar(value="Points : —")
        self.stat_vertices = tk.StringVar(value="Sommets : —")
        self.stat_regions = tk.StringVar(value="Régions finies : —")

        for var in (self.stat_points, self.stat_vertices, self.stat_regions):
            ttk.Label(stats_frame, textvariable=var, anchor=tk.W).pack(
                fill=tk.X, pady=1
            )

        # ── Options d'affichage ───────────────────────────────────────
        opts_frame = ttk.LabelFrame(panel, text="Affichage", padding=8)
        opts_frame.pack(fill=tk.X, pady=(0, 8))

        self.opt_color = tk.BooleanVar(value=True)
        self.opt_labels = tk.BooleanVar(value=True)
        self.opt_vertices = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            opts_frame, text="Colorier les cellules",
            variable=self.opt_color, command=self._redraw,
        ).pack(anchor=tk.W, pady=1)
        ttk.Checkbutton(
            opts_frame, text="Afficher les étiquettes",
            variable=self.opt_labels, command=self._redraw,
        ).pack(anchor=tk.W, pady=1)
        ttk.Checkbutton(
            opts_frame, text="Afficher les sommets",
            variable=self.opt_vertices, command=self._redraw,
        ).pack(anchor=tk.W, pady=1)

        # ── Aide navigation ───────────────────────────────────────────
        nav_frame = ttk.LabelFrame(panel, text="Navigation", padding=8)
        nav_frame.pack(fill=tk.X)

        hints = [
            "Molette      : zoom",
            "Glisser      : deplacer",
            "Double-clic  : vue initiale",
        ]
        for hint in hints:
            ttk.Label(nav_frame, text=hint, style="Hint.TLabel", anchor=tk.W).pack(
                fill=tk.X, pady=1
            )

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(
            label="Ouvrir...", accelerator="Ctrl+O", command=self._open_file
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exporter en SVG...", command=self._export_svg)
        file_menu.add_command(label="Exporter en image...", command=self._export_image)
        file_menu.add_separator()
        file_menu.add_command(
            label="Quitter", accelerator="Ctrl+Q", command=self.quit
        )

        help_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="A propos", command=self._show_about)

        self.bind("<Control-o>", lambda _e: self._open_file())
        self.bind("<Control-q>", lambda _e: self.quit())

    # ------------------------------------------------------------------
    # Actions principales
    # ------------------------------------------------------------------

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier de points",
            filetypes=[
                ("Fichiers texte", "*.txt"),
                ("Tous les fichiers", "*.*"),
            ],
        )
        if not path:
            return

        try:
            self._points = parse_points_file(path)
            self._vor = compute_voronoi(self._points)
            self.canvas_widget.plot(self._vor, self._get_draw_options())
            self.toolbar.enable_export()
            self._update_stats()
            filename = path.replace("\\", "/").split("/")[-1]
            self._set_status(
                f"{len(self._points)} point(s) chargé(s) depuis « {filename} »  —  "
                f"{len(self._vor.vertices)} sommet(s) de Voronoï"
            )
        except (FileNotFoundError, ValueError) as exc:
            messagebox.showerror("Erreur de chargement", str(exc))
            self._set_status("Erreur lors du chargement du fichier.")

    def _export_svg(self) -> None:
        if self._vor is None:
            messagebox.showwarning("Aucun diagramme", "Chargez d'abord un fichier de points.")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter en SVG",
            defaultextension=".svg",
            filetypes=[("SVG", "*.svg")],
        )
        if not path:
            return
        try:
            export_svg(self.canvas_widget.get_figure(), path)
            self._set_status(f"SVG exporté : {path}")
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror("Erreur d'export SVG", str(exc))

    def _export_image(self) -> None:
        if self._vor is None:
            messagebox.showwarning("Aucun diagramme", "Chargez d'abord un fichier de points.")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter en image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return
        try:
            export_image(self.canvas_widget.get_figure(), path)
            self._set_status(f"Image exportée : {path}")
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror("Erreur d'export image", str(exc))

    def _reset_view(self) -> None:
        self.canvas_widget.reset_view()

    def _show_about(self) -> None:
        messagebox.showinfo(
            "A propos",
            "Diagramme de Voronoï  —  v1.1\n\n"
            "Bibliothèques utilisées :\n"
            "  • scipy      → calcul du diagramme\n"
            "  • matplotlib → visualisation & export\n"
            "  • numpy      → manipulation des données\n"
            "  • tkinter    → interface graphique\n\n"
            "Formats de fichier acceptés :\n"
            "  x,y  |  x;y  |  x y\n"
            "  (une paire de coordonnées par ligne)\n"
            "  Les lignes commençant par '#' sont ignorées.\n\n"
            "Navigation :\n"
            "  Molette     → zoom centré sur le curseur\n"
            "  Glisser     → déplacer la vue\n"
            "  Double-clic → vue initiale",
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_draw_options(self) -> DrawOptions:
        return DrawOptions(
            show_points=True,
            show_vertices=self.opt_vertices.get(),
            show_labels=self.opt_labels.get(),
            color_cells=self.opt_color.get(),
        )

    def _redraw(self) -> None:
        """Appelé par les checkboxes : redessine avec les options courantes."""
        if self._vor is not None:
            self.canvas_widget.redraw(self._get_draw_options())

    def _update_stats(self) -> None:
        """Met à jour le panneau de statistiques."""
        n_finite = sum(1 for r in self._vor.regions if r and -1 not in r)
        self.stat_points.set(f"Points : {len(self._points)}")
        self.stat_vertices.set(f"Sommets : {len(self._vor.vertices)}")
        self.stat_regions.set(f"Régions finies : {n_finite}")

    def _set_status(self, msg: str) -> None:
        """Met à jour le message principal de la barre de statut."""
        self._main_status = msg
        self.status_var.set(msg)

    def _on_mouse_move(self, event) -> None:
        """Affiche les coordonnées dans la barre de statut au survol."""
        if event.inaxes:
            self.status_var.set(
                f"  x = {event.xdata:.3f}      y = {event.ydata:.3f}"
            )

    def _on_axes_leave(self, _event) -> None:
        """Restaure le message principal quand la souris quitte l'axe."""
        self.status_var.set(self._main_status)
