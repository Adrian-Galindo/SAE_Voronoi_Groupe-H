"""Export du diagramme en format SVG."""
from matplotlib.figure import Figure


def export_svg(figure: Figure, filepath: str) -> None:
    """
    Sauvegarde la figure Matplotlib sous forme de fichier SVG.

    Args:
        figure  : la figure Matplotlib à exporter.
        filepath: chemin complet du fichier de destination (ex: /tmp/voronoi.svg).
    """
    figure.savefig(
        filepath,
        format="svg",
        bbox_inches="tight",
        facecolor="white",
    )
