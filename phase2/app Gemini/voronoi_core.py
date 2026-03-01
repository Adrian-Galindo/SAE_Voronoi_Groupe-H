import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial.qhull import QhullError
from typing import Optional, Tuple

def load_points_from_file(filepath: str) -> np.ndarray:
    """
    Lit un fichier texte contenant des paires de coordonnées (x,y) séparées par des virgules.
    
    Args:
        filepath (str): Le chemin vers le fichier texte.
        
    Returns:
        np.ndarray: Un tableau numpy contenant les coordonnées des points.
        
    Raises:
        ValueError: Si le fichier est mal formaté ou contient des données non numériques.
        FileNotFoundError: Si le fichier n'existe pas.
    """
    try:
        # Lecture du fichier en ignorant les lignes vides
        points = np.loadtxt(filepath, delimiter=',', dtype=float)

        if points.ndim == 1 and len(points) == 2:
            points = points.reshape(1, 2) # Cas d'un seul point
        elif points.ndim != 2 or points.shape[1] != 2:
            raise ValueError("Le fichier doit contenir exactement deux colonnes (x, y).")

        return points
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier : {e}")

def compute_voronoi(points: np.ndarray) -> Tuple[Optional[Voronoi], str]:
    """
    Calcule le diagramme de Voronoï à partir d'un ensemble de points.
    
    Args:
        points (np.ndarray): Tableau numpy de forme (N, 2) contenant les points.
        
    Returns:
        Tuple[Optional[Voronoi], str]: Un tuple contenant l'objet Voronoi (ou None si échec)
        et un message d'erreur éventuel.
    """
    if len(points) < 4:
        return None, "Au moins 4 points non colinéaires sont nécessaires pour un diagramme de Voronoï standard."

    try:
        vor = Voronoi(points)
        return vor, ""
    except QhullError:
        return None, "Erreur de calcul : les points sont peut-être colinéaires ou superposés."
    except Exception as e:
        return None, f"Erreur inattendue : {e}"