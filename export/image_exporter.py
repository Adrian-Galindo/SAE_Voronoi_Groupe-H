"""Export du diagramme en format image (PNG / JPG)."""
from pathlib import Path
from matplotlib.figure import Figure


def export_image(figure: Figure, filepath: str, dpi: int = 150) -> None:
    """
    Sauvegarde la figure Matplotlib sous forme d'image PNG ou JPEG.

    Le format est inféré depuis l'extension du fichier :
        .png  → PNG
        .jpg / .jpeg → JPEG

    Args:
        figure  : la figure Matplotlib à exporter.
        filepath: chemin complet du fichier de destination.
        dpi     : résolution en points par pouce (défaut : 150).
    """
    ext = Path(filepath).suffix.lower().lstrip(".")
    fmt = "jpeg" if ext in ("jpg", "jpeg") else "png"

    figure.savefig(
        filepath,
        format=fmt,
        bbox_inches="tight",
        facecolor="white",
        dpi=dpi,
    )
