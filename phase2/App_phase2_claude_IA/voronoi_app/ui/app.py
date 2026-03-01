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
        self._statut_principal = "Prêt  —  Ouvrez un fichier de points."

        # Variables du panneau latéral (affectées dans _construire_panneau_lateral)
        self.stat_points: tk.StringVar
        self.stat_regions: tk.StringVar
        self.opt_color: tk.BooleanVar
        self.opt_labels: tk.BooleanVar

        self._configurer_theme()
        self._construire_interface()

    # ── Thème et construction de l'interface ──────────────────────────────────

    def _configurer_theme(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabelframe", background="#f4f6f9", bordercolor="#d0d7e2")
        style.configure("TLabelframe.Label", font=("Helvetica", 9, "bold"),
                        foreground="#1e3a5f", background="#f4f6f9")
        style.configure("Stat.TLabel", font=("Helvetica", 9), foreground="#2c3e50",
                        background="#f4f6f9")
        style.configure("Hint.TLabel", foreground="#6c757d", font=("Helvetica", 8),
                        background="#f4f6f9")
        style.configure("TCheckbutton", background="#f4f6f9")

    def _construire_interface(self) -> None:
        self._construire_menu()

        callbacks = {
            "open": self._charger_fichier_points,
            "export_svg": self._exporter_en_svg,
            "export_image": self._exporter_en_image,
            "reset_view": self._reinitialiser_vue,
            "about": self._afficher_a_propos,
        }
        self.toolbar = Toolbar(self, callbacks=callbacks)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas_widget = VoronoiCanvas(main_frame)
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self._construire_panneau_lateral(main_frame)

        self.status_var = tk.StringVar(value=self._statut_principal)
        status_bar = ttk.Label(
            self, textvariable=self.status_var,
            relief=tk.SUNKEN, anchor=tk.W, padding=(8, 2),
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.canvas_widget.mpl_canvas.mpl_connect(
            "motion_notify_event", self._sur_deplacement_souris
        )
        self.canvas_widget.mpl_canvas.mpl_connect(
            "axes_leave_event", self._sur_sortie_axe
        )

    def _construire_panneau_lateral(self, parent) -> None:
        """Construit le panneau latéral droit : statistiques, options, aide."""
        panel = tk.Frame(parent, width=200, bg="#f4f6f9",
                         highlightbackground="#d0d7e2", highlightthickness=1)
        panel.pack(fill=tk.Y, side=tk.RIGHT, padx=(6, 0))
        panel.pack_propagate(False)

        # ── Statistiques ──────────────────────────────────────────────
        stats_frame = ttk.LabelFrame(panel, text="Statistiques", padding=(10, 6))
        stats_frame.pack(fill=tk.X, padx=8, pady=(10, 6))

        self.stat_points = tk.StringVar(value="Points : —")
        self.stat_regions = tk.StringVar(value="Régions finies : —")

        self._creer_ligne_statistique(stats_frame, "#c0392b", self.stat_points)
        self._creer_ligne_statistique(stats_frame, "#1a6faf", self.stat_regions)

        # ── Options d'affichage ───────────────────────────────────────
        opts_frame = ttk.LabelFrame(panel, text="Affichage", padding=(10, 6))
        opts_frame.pack(fill=tk.X, padx=8, pady=(0, 6))

        self.opt_color = tk.BooleanVar(value=True)
        self.opt_labels = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            opts_frame, text="Colorier les cellules",
            variable=self.opt_color, command=self._redessiner_diagramme,
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            opts_frame, text="Afficher les étiquettes",
            variable=self.opt_labels, command=self._redessiner_diagramme,
        ).pack(anchor=tk.W, pady=2)

        # ── Aide navigation ───────────────────────────────────────────
        nav_frame = ttk.LabelFrame(panel, text="Navigation", padding=(10, 6))
        nav_frame.pack(fill=tk.X, padx=8)

        for hint in ["Molette      : zoom", "Glisser      : déplacer",
                     "Double-clic  : vue initiale"]:
            ttk.Label(nav_frame, text=hint, style="Hint.TLabel", anchor=tk.W).pack(
                fill=tk.X, pady=1
            )

    def _creer_ligne_statistique(self, parent, couleur_point: str,
                                  var_texte: tk.StringVar) -> None:
        """Crée une ligne de statistique avec un indicateur coloré."""
        row = tk.Frame(parent, bg="#f4f6f9")
        row.pack(fill=tk.X, pady=3)
        dot = tk.Frame(row, bg=couleur_point, width=9, height=9)
        dot.pack(side=tk.LEFT, padx=(0, 8))
        dot.pack_propagate(False)
        ttk.Label(row, textvariable=var_texte, style="Stat.TLabel", anchor=tk.W).pack(
            side=tk.LEFT, fill=tk.X
        )

    def _construire_menu(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        fichier_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)
        fichier_menu.add_command(
            label="Ouvrir...", accelerator="Ctrl+O",
            command=self._charger_fichier_points,
        )
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Exporter en SVG...",
                                 command=self._exporter_en_svg)
        fichier_menu.add_command(label="Exporter en image...",
                                 command=self._exporter_en_image)
        fichier_menu.add_separator()
        fichier_menu.add_command(
            label="Quitter", accelerator="Ctrl+Q", command=self.quit
        )

        aide_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Aide", menu=aide_menu)
        aide_menu.add_command(label="À propos", command=self._afficher_a_propos)

        self.bind("<Control-o>", lambda _e: self._charger_fichier_points())
        self.bind("<Control-q>", lambda _e: self.quit())

    # ── Actions principales ───────────────────────────────────────────────────

    def _charger_fichier_points(self) -> None:
        """Ouvre un fichier de coordonnées et affiche le diagramme correspondant."""
        chemin = filedialog.askopenfilename(
            title="Ouvrir un fichier de points",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if not chemin:
            return

        try:
            self._points = parse_points_file(chemin)
            self._vor = compute_voronoi(self._points)
            self.canvas_widget.afficher_diagramme(self._vor, self._construire_options_rendu())
            self.toolbar.activer_export()
            self._actualiser_statistiques()
            nom_fichier = chemin.replace("\\", "/").split("/")[-1]
            self._mettre_a_jour_statut(
                f"{len(self._points)} point(s) chargé(s) depuis « {nom_fichier} »"
            )
        except (FileNotFoundError, ValueError) as exc:
            messagebox.showerror("Erreur de chargement", str(exc))
            self._mettre_a_jour_statut("Erreur lors du chargement du fichier.")

    def _exporter_en_svg(self) -> None:
        """Enregistre le diagramme courant au format SVG."""
        if self._vor is None:
            messagebox.showwarning("Aucun diagramme",
                                   "Chargez d'abord un fichier de points.")
            return
        chemin = filedialog.asksaveasfilename(
            title="Exporter en SVG",
            defaultextension=".svg",
            filetypes=[("SVG", "*.svg")],
        )
        if not chemin:
            return
        try:
            export_svg(self.canvas_widget.obtenir_figure(), chemin)
            self._mettre_a_jour_statut(f"SVG exporté : {chemin}")
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror("Erreur d'export SVG", str(exc))

    def _exporter_en_image(self) -> None:
        """Enregistre le diagramme courant au format PNG ou JPG."""
        if self._vor is None:
            messagebox.showwarning("Aucun diagramme",
                                   "Chargez d'abord un fichier de points.")
            return
        chemin = filedialog.asksaveasfilename(
            title="Exporter en image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"),
                       ("Tous les fichiers", "*.*")],
        )
        if not chemin:
            return
        try:
            export_image(self.canvas_widget.obtenir_figure(), chemin)
            self._mettre_a_jour_statut(f"Image exportée : {chemin}")
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror("Erreur d'export image", str(exc))

    def _reinitialiser_vue(self) -> None:
        """Recentre la vue du canvas sur l'étendue initiale."""
        self.canvas_widget.reinitialiser_vue()

    def _afficher_a_propos(self) -> None:
        """Affiche la boîte de dialogue « À propos »."""
        messagebox.showinfo(
            "À propos",
            "Diagramme de Voronoï — SAE R6A01\n\n"
            "Bibliothèques utilisées :\n"
            "  • scipy      → calcul du diagramme\n"
            "  • matplotlib → visualisation & export\n"
            "  • numpy      → manipulation des données\n"
            "  • tkinter    → interface graphique\n\n"
            "Formats de fichier acceptés :\n"
            "  x,y  |  x;y  |  x y\n"
            "  (une paire de coordonnées par ligne)\n\n"
            "Navigation :\n"
            "  Molette     → zoom centré sur le curseur\n"
            "  Glisser     → déplacer la vue\n"
            "  Double-clic → vue initiale",
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _construire_options_rendu(self) -> DrawOptions:
        """Construit les options de rendu à partir des cases à cocher."""
        return DrawOptions(
            show_points=True,
            show_vertices=False,
            show_labels=self.opt_labels.get(),
            color_cells=self.opt_color.get(),
        )

    def _redessiner_diagramme(self) -> None:
        """Redessine le diagramme avec les options d'affichage courantes."""
        if self._vor is not None:
            self.canvas_widget.redessiner(self._construire_options_rendu())

    def _actualiser_statistiques(self) -> None:
        """Met à jour les compteurs du panneau statistiques."""
        n_finies = sum(1 for r in self._vor.regions if r and -1 not in r)
        self.stat_points.set(f"Points : {len(self._points)}")
        self.stat_regions.set(f"Régions finies : {n_finies}")

    def _mettre_a_jour_statut(self, message: str) -> None:
        """Affiche un message dans la barre de statut et le mémorise."""
        self._statut_principal = message
        self.status_var.set(message)

    def _sur_deplacement_souris(self, event) -> None:
        """Affiche les coordonnées du curseur dans la barre de statut."""
        if event.inaxes:
            self.status_var.set(
                f"  x = {event.xdata:.3f}      y = {event.ydata:.3f}"
            )

    def _sur_sortie_axe(self, _event) -> None:
        """Restaure le message principal quand le curseur quitte l'axe."""
        self.status_var.set(self._statut_principal)
