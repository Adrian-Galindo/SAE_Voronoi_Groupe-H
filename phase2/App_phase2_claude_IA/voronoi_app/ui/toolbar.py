"""Barre d'outils de l'application — design moderne."""
import tkinter as tk


class Toolbar(tk.Frame):  # pylint: disable=too-many-ancestors
    """Barre d'outils avec fond coloré et boutons stylisés."""

    _FOND = "#1e3a5f"
    _COULEUR_SEP = "#2d527a"

    _COULEURS = {
        "primaire":  ("#2e86de", "#1a6bbf"),
        "succes":    ("#20bf6b", "#0ea558"),
        "neutre":    ("#4a5568", "#374151"),
        "discret":   ("#6c757d", "#565e65"),
        "desactive": ("#354d63", "#354d63"),
    }

    _STYLE_BTN = {
        "relief": tk.FLAT,
        "font": ("Helvetica", 9, "bold"),
        "padx": 14,
        "pady": 6,
        "borderwidth": 0,
        "highlightthickness": 0,
    }

    def __init__(self, parent, callbacks: dict, **kwargs):
        super().__init__(parent, bg=self._FOND, pady=2, **kwargs)
        self._callbacks = callbacks
        self._construire_barre()

    # ── Construction ──────────────────────────────────────────────────────────

    def _creer_bouton(self, texte: str, cle_couleur: str, commande) -> tk.Button:
        bg, abg = self._COULEURS[cle_couleur]
        return tk.Button(
            self, text=texte, command=commande,
            bg=bg, fg="white",
            activebackground=abg, activeforeground="white",
            cursor="hand2",
            **self._STYLE_BTN,
        )

    def _ajouter_separateur(self) -> None:
        tk.Frame(self, bg=self._COULEUR_SEP, width=1).pack(
            side=tk.LEFT, fill=tk.Y, padx=10, pady=5
        )

    def _construire_barre(self) -> None:
        tk.Frame(self, bg=self._FOND, width=8).pack(side=tk.LEFT)

        self._btn_ouvrir = self._creer_bouton(
            "▶  Ouvrir fichier", "primaire",
            self._callbacks.get("open", lambda: None),
        )
        self._btn_ouvrir.pack(side=tk.LEFT, padx=(0, 4), pady=5)

        self._ajouter_separateur()

        self._btn_svg = self._creer_bouton(
            "▲  Exporter SVG", "succes",
            self._callbacks.get("export_svg", lambda: None),
        )
        self._btn_svg.pack(side=tk.LEFT, padx=(0, 4), pady=5)

        self._btn_image = self._creer_bouton(
            "▲  Exporter image", "succes",
            self._callbacks.get("export_image", lambda: None),
        )
        self._btn_image.pack(side=tk.LEFT, padx=(0, 4), pady=5)

        self._ajouter_separateur()

        self._btn_vue = self._creer_bouton(
            "↺  Vue initiale", "neutre",
            self._callbacks.get("reset_view", lambda: None),
        )
        self._btn_vue.pack(side=tk.LEFT, padx=(0, 4), pady=5)

        self._ajouter_separateur()

        self._btn_apropos = self._creer_bouton(
            "i  À propos", "discret",
            self._callbacks.get("about", lambda: None),
        )
        self._btn_apropos.pack(side=tk.LEFT, padx=(0, 4), pady=5)

        self._desactiver_bouton(self._btn_svg)
        self._desactiver_bouton(self._btn_image)
        self._desactiver_bouton(self._btn_vue)

    # ── Gestion des états ─────────────────────────────────────────────────────

    def _desactiver_bouton(self, btn: tk.Button) -> None:
        bg, _ = self._COULEURS["desactive"]
        btn.config(
            state=tk.DISABLED, bg=bg,
            activebackground=bg, fg="#8a9aaa", cursor="",
        )

    def _activer_bouton(self, btn: tk.Button, cle_couleur: str) -> None:
        bg, abg = self._COULEURS[cle_couleur]
        btn.config(
            state=tk.NORMAL, bg=bg,
            activebackground=abg, fg="white", cursor="hand2",
        )

    # ── API publique ──────────────────────────────────────────────────────────

    def activer_export(self) -> None:
        """Active les boutons d'export et de réinitialisation de vue."""
        self._activer_bouton(self._btn_svg, "succes")
        self._activer_bouton(self._btn_image, "succes")
        self._activer_bouton(self._btn_vue, "neutre")

    def desactiver_export(self) -> None:
        """Désactive les boutons d'export et de réinitialisation de vue."""
        self._desactiver_bouton(self._btn_svg)
        self._desactiver_bouton(self._btn_image)
        self._desactiver_bouton(self._btn_vue)
