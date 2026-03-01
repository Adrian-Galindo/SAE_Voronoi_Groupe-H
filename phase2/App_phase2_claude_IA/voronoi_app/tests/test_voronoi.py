"""Tests unitaires — core/voronoi.py."""
import pytest

from core.voronoi import compute_voronoi

_POINTS_VALIDES = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0), (2.0, 2.0), (3.0, 0.0)]


# ── Structure du diagramme ────────────────────────────────────────────────────

def test_should_return_voronoi_object_given_valid_points():
    # Arrangement
    points = _POINTS_VALIDES

    # Action
    diagramme = compute_voronoi(points)

    # Assertion
    assert diagramme is not None


def test_should_preserve_all_input_points_given_valid_list():
    # Arrangement
    points = _POINTS_VALIDES

    # Action
    diagramme = compute_voronoi(points)

    # Assertion
    assert len(diagramme.points) == len(points)


def test_should_generate_vertices_given_non_collinear_points():
    # Arrangement
    points = _POINTS_VALIDES

    # Action
    diagramme = compute_voronoi(points)

    # Assertion
    assert len(diagramme.vertices) > 0


def test_should_generate_ridges_given_valid_points():
    # Arrangement
    points = _POINTS_VALIDES

    # Action
    diagramme = compute_voronoi(points)

    # Assertion
    assert len(diagramme.ridge_vertices) > 0


# ── Cas d'erreur ──────────────────────────────────────────────────────────────

def test_should_raise_value_error_given_duplicate_points():
    # Arrangement
    points_avec_doublon = [(0, 0), (1, 0), (0, 0), (2, 2)]

    # Action & Assertion
    with pytest.raises(ValueError, match="dupliqué"):
        compute_voronoi(points_avec_doublon)


def test_should_raise_value_error_given_collinear_points():
    # Arrangement
    points_colineaires = [(0, 0), (1, 1), (2, 2), (3, 3)]

    # Action & Assertion
    with pytest.raises(ValueError, match="colinéaires"):
        compute_voronoi(points_colineaires)


def test_should_accept_minimum_three_points_given_non_collinear_triangle():
    # Arrangement
    triangle = [(0, 0), (3, 0), (1.5, 2)]

    # Action
    diagramme = compute_voronoi(triangle)

    # Assertion
    assert len(diagramme.points) == 3
