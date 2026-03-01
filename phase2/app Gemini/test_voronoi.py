import pytest
import numpy as np
import tempfile
import os
from voronoi_core import load_points_from_file, compute_voronoi

@pytest.fixture
def temp_data_file():
    """Fixture pour créer un fichier de points temporaire."""
    content = "1.0,2.0\n3.5,4.1\n5.0,1.0\n2.0,6.0\n8.0,3.0"
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    yield path
    os.remove(path)

@pytest.fixture
def invalid_data_file():
    """Fixture pour créer un fichier avec des données invalides."""
    content = "1.0,2.0\ninvalide,data\n5.0,1.0"
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    yield path
    os.remove(path)

def test_load_points_valid(temp_data_file):
    """Teste le chargement réussi des points."""
    points = load_points_from_file(temp_data_file)
    assert isinstance(points, np.ndarray)
    assert points.shape == (5, 2)
    assert points[0, 0] == 1.0

def test_load_points_invalid(invalid_data_file):
    """Teste la gestion d'erreur lors d'un fichier mal formaté."""
    with pytest.raises(ValueError, match="Erreur lors de la lecture du fichier"):
        load_points_from_file(invalid_data_file)

def test_compute_voronoi_success():
    """Teste la création d'un diagramme valide."""
    points = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0.5, 0.5]])
    vor, error = compute_voronoi(points)
    assert vor is not None
    assert error == ""
    assert hasattr(vor, 'regions')

def test_compute_voronoi_insufficient_points():
    """Teste la création avec trop peu de points."""
    points = np.array([[0, 0], [1, 1]])
    vor, error = compute_voronoi(points)
    assert vor is None
    assert "Au moins 4 points" in error

def test_compute_voronoi_collinear():
    """Teste la création avec des points colinéaires (impossible)."""
    points = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
    vor, error = compute_voronoi(points)
    assert vor is None
    assert "colinéaires" in error