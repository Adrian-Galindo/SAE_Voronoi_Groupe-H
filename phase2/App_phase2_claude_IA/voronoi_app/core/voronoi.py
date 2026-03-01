"""Calcul du diagramme de Voronoï via scipy."""
import numpy as np
from scipy.spatial import Voronoi  # pylint: disable=no-name-in-module


def compute_voronoi(points: list[tuple[float, float]]) -> Voronoi:
    """
    Calcule le diagramme de Voronoï à partir d'une liste de points 2D.

    Args:
        points: liste de tuples (x, y).

    Returns:
        Un objet scipy.spatial.Voronoi.

    Raises:
        ValueError: si des points sont dupliqués ou tous colinéaires.
    """
    pts = np.array(points, dtype=float)

    pts_uniques = np.unique(pts, axis=0)
    if len(pts_uniques) < len(pts):
        n_doublons = len(pts) - len(pts_uniques)
        raise ValueError(
            f"{n_doublons} point(s) dupliqué(s) détecté(s). "
            "Veuillez fournir des points distincts."
        )

    # Détection de la colinéarité par décomposition en valeurs singulières (SVD)
    centree = pts - pts.mean(axis=0)
    _, sv, _ = np.linalg.svd(centree)
    if sv[1] < 1e-10 * sv[0]:
        raise ValueError(
            "Tous les points sont colinéaires. "
            "Le diagramme de Voronoï ne peut pas être calculé."
        )

    return Voronoi(pts)
