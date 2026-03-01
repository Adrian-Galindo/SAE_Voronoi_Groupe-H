import os
import pytest
import numpy as np
from matplotlib.figure import Figure
from scipy.spatial import Voronoi

from app.io_utils import read_points
from app.voronoi_engine import compute_voronoi, voronoi_finite_polygons_2d, plot_voronoi_colored
from app.exporter import export_diagram


# ==========================================
# TESTS : io_utils.py (Lecture de fichiers)
# ==========================================

def test_read_points_valid(tmp_path):
    """Test la lecture correcte d'un fichier de points."""
    # Création d'un fichier temporaire valide
    test_file = tmp_path / "valid_points.txt"
    test_file.write_text("1,1\n2,4\n3.5,2.1\n")

    points = read_points(str(test_file))

    assert len(points) == 3
    assert points[0] == (1.0, 1.0)
    assert points[2] == (3.5, 2.1)

def test_read_points_invalid_format(tmp_path):
    """Test si une erreur est levée quand le format est mauvais."""
    test_file = tmp_path / "invalid_points.txt"
    test_file.write_text("1,1\n2;4\n3,2\n") # Le point 2 utilise un point-virgule

    with pytest.raises(ValueError, match="Invalid format"):
        read_points(str(test_file))

def test_read_points_too_few(tmp_path):
    """Test si une erreur est levée quand il y a moins de 3 points."""
    test_file = tmp_path / "few_points.txt"
    test_file.write_text("1,1\n2,4\n")

    with pytest.raises(ValueError, match="At least 3 points required"):
        read_points(str(test_file))


# ==========================================
# TESTS : voronoi_engine.py (Calcul & Rendu)
# ==========================================

def test_compute_voronoi_valid():
    """Test le calcul du diagramme avec des points valides."""
    points = [(1, 1), (2, 4), (3, 2), (4, 5)]
    vor = compute_voronoi(points)

    assert isinstance(vor, Voronoi)
    assert len(vor.points) == 4

def test_compute_voronoi_invalid():
    """Test le calcul avec trop peu de points."""
    points = [(1, 1), (2, 2)]
    with pytest.raises(ValueError, match="At least 3 points required"):
        compute_voronoi(points)

def test_voronoi_finite_polygons_2d():
    """Test la fermeture des polygones infinis."""
    points = [(1, 1), (1, 5), (5, 1), (5, 5), (3, 3)]
    vor = compute_voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)

    # Il doit y avoir autant de régions fermées que de points d'entrée (5)
    assert len(regions) == 5
    # Vérifie que les sommets ne contiennent plus l'indice -1 (qui représente l'infini)
    for region in regions:
        assert -1 not in region

def test_plot_voronoi_colored():
    """Test que la fonction de dessin retourne bien une figure matplotlib."""
    points = [(1, 1), (2, 4), (3, 2)]
    vor = compute_voronoi(points)
    fig = plot_voronoi_colored(vor)

    assert isinstance(fig, Figure)


# ==========================================
# TESTS : exporter.py (Sauvegarde d'images)
# ==========================================

def test_export_diagram_valid(tmp_path):
    """Test l'exportation vers un format supporté (PNG et SVG)."""
    points = [(1, 1), (2, 4), (3, 2)]
    vor = compute_voronoi(points)

    png_path = str(tmp_path / "test.png")
    svg_path = str(tmp_path / "test.svg")

    export_diagram(vor, png_path)
    export_diagram(vor, svg_path)

    assert os.path.exists(png_path)
    assert os.path.exists(svg_path)

def test_export_diagram_invalid(tmp_path):
    """Test le rejet d'un format non supporté."""
    points = [(1, 1), (2, 4), (3, 2)]
    vor = compute_voronoi(points)
    bad_path = str(tmp_path / "test.pdf")

    with pytest.raises(ValueError, match="Unsupported format"):
        export_diagram(vor, bad_path)