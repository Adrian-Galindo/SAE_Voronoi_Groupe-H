"""Lecture et validation du fichier de points."""
import re
from pathlib import Path


def parse_points_file(filepath: str) -> list[tuple[float, float]]:
    """
    Parse un fichier texte contenant une paire de coordonnées par ligne.

    Formats acceptés par ligne :
        - "x,y"   ex : 2,4  ou  5.3,4.5
        - "x;y"   ex : 2;4
        - "x y"   ex : 2 4

    Les lignes vides et les lignes commençant par '#' sont ignorées.

    Raises:
        FileNotFoundError : si le fichier n'existe pas.
        ValueError        : si une ligne est mal formée ou si moins
                            de 3 points valides sont trouvés.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    points: list[tuple[float, float]] = []

    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = re.split(r"[,;\s]+", line)
            if len(parts) != 2:
                raise ValueError(
                    f"Ligne {lineno} : format invalide « {line} »\n"
                    "Format attendu : « x,y »  (ex : 2.5,3.0)"
                )
            try:
                x, y = float(parts[0]), float(parts[1])
            except ValueError as exc:
                raise ValueError(
                    f"Ligne {lineno} : impossible de convertir "
                    f"« {line} » en coordonnées numériques."
                ) from exc
            points.append((x, y))

    if len(points) < 3:
        raise ValueError(
            f"Seulement {len(points)} point(s) chargé(s). "
            "Au moins 3 points non colinéaires sont requis pour "
            "construire un diagramme de Voronoï."
        )

    return points
