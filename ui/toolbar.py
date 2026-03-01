"""Barre d'outils de l'application."""
import tkinter as tk
from tkinter import ttk


class Toolbar(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Frame contenant les boutons d'action principaux."""

    def __init__(self, parent, callbacks: dict, **kwargs):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1, **kwargs)
        self._callbacks = callbacks
        self._build()

    def _build(self) -> None:
        self._btn_open = ttk.Button(
            self, text="Ouvrir fichier",
            command=self._callbacks.get("open", lambda: None),
        )
        self._btn_open.pack(side=tk.LEFT, padx=5, pady=4)

        ttk.Separator(self, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=6, pady=4
        )

        self._btn_svg = ttk.Button(
            self, text="Exporter SVG",
            command=self._callbacks.get("export_svg", lambda: None),
            state=tk.DISABLED,
        )
        self._btn_svg.pack(side=tk.LEFT, padx=5, pady=4)

        self._btn_img = ttk.Button(
            self, text="Exporter image",
            command=self._callbacks.get("export_image", lambda: None),
            state=tk.DISABLED,
        )
        self._btn_img.pack(side=tk.LEFT, padx=5, pady=4)

        ttk.Separator(self, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=6, pady=4
        )

        self._btn_reset = ttk.Button(
            self, text="Vue initiale",
            command=self._callbacks.get("reset_view", lambda: None),
            state=tk.DISABLED,
        )
        self._btn_reset.pack(side=tk.LEFT, padx=5, pady=4)

        ttk.Separator(self, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=6, pady=4
        )

        self._btn_about = ttk.Button(
            self, text="A propos",
            command=self._callbacks.get("about", lambda: None),
        )
        self._btn_about.pack(side=tk.LEFT, padx=5, pady=4)

    def enable_export(self) -> None:
        """Active les boutons d'export et de réinitialisation."""
        self._btn_svg.config(state=tk.NORMAL)
        self._btn_img.config(state=tk.NORMAL)
        self._btn_reset.config(state=tk.NORMAL)

    def disable_export(self) -> None:
        """Désactive les boutons d'export et de réinitialisation."""
        self._btn_svg.config(state=tk.DISABLED)
        self._btn_img.config(state=tk.DISABLED)
        self._btn_reset.config(state=tk.DISABLED)
