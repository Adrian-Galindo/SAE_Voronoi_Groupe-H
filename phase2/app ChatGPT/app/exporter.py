from scipy.spatial import Voronoi
from voronoi_engine import plot_voronoi_colored


def export_diagram(vor: Voronoi, filename: str) -> None:
    fig = plot_voronoi_colored(vor)

    if filename.lower().endswith(".svg"):
        fig.savefig(filename, format="svg")
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        fig.savefig(filename)
    else:
        raise ValueError("Unsupported format.")

    fig.clf()