"""Tests unitaires pour core/voronoi.py."""
import pytest

from core.voronoi import compute_voronoi

BASIC_POINTS = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0), (2.0, 2.0), (3.0, 0.0)]


def test_returns_voronoi_object():
    vor = compute_voronoi(BASIC_POINTS)
    assert vor is not None


def test_correct_number_of_points():
    vor = compute_voronoi(BASIC_POINTS)
    assert len(vor.points) == len(BASIC_POINTS)


def test_has_vertices():
    vor = compute_voronoi(BASIC_POINTS)
    assert len(vor.vertices) > 0


def test_has_ridges():
    vor = compute_voronoi(BASIC_POINTS)
    assert len(vor.ridge_vertices) > 0


def test_duplicate_points_raise():
    with pytest.raises(ValueError, match="dupliqué"):
        compute_voronoi([(0, 0), (1, 0), (0, 0), (2, 2)])


def test_collinear_points_raise():
    with pytest.raises(ValueError, match="colinéaires"):
        compute_voronoi([(0, 0), (1, 1), (2, 2), (3, 3)])


def test_minimum_three_points():
    vor = compute_voronoi([(0, 0), (3, 0), (1.5, 2)])
    assert len(vor.points) == 3
