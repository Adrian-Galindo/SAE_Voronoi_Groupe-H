"""Calcul du diagramme de Voronoï via scipy."""
import numpy as np
from scipy.spatial import Voronoi 


def compute_voronoi(points: list[tuple[float, float]]) -> Voronoi:
    """
    Calcule le diagramme de Voronoï à partir d'une liste de points 2D.

    Args:
        points: liste de tuples (x, y).

    Returns:
        Un objet scipy.spatial.Voronoi.

    Raises:
        ValueError: points dupliqués ou tous colinéaires.
    """
    pts = np.array(points, dtype=float)

    # Vérification des doublons
    unique_pts = np.unique(pts, axis=0)
    if len(unique_pts) < len(pts):
        n_dup = len(pts) - len(unique_pts)
        raise ValueError(
            f"{n_dup} point(s) dupliqué(s) détecté(s). "
            "Veuillez fournir des points distincts."
        )

    # Vérification de la colinéarité (SVD sur la matrice centrée)
    centered = pts - pts.mean(axis=0)
    _, sv, _ = np.linalg.svd(centered)
    if sv[1] < 1e-10 * sv[0]:
        raise ValueError(
            "Tous les points sont colinéaires. "
            "Le diagramme de Voronoï ne peut pas être calculé."
        )

    return Voronoi(pts)
