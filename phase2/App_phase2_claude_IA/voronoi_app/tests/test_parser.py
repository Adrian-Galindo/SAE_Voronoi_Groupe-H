"""Tests unitaires — core/parser.py."""
import os
import tempfile

import pytest

from core.parser import parse_points_file


def _creer_fichier_temporaire(contenu: str) -> str:
    """Crée un fichier texte temporaire avec le contenu donné et retourne son chemin."""
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(contenu)
    f.close()
    return f.name


# ── Séparateurs acceptés ──────────────────────────────────────────────────────

def test_should_parse_all_points_given_comma_separator():
    # Arrangement
    path = _creer_fichier_temporaire("1,2\n3.5,4.0\n5,6\n")

    # Action
    points = parse_points_file(path)
    os.unlink(path)

    # Assertion
    assert points == [(1.0, 2.0), (3.5, 4.0), (5.0, 6.0)]


def test_should_parse_first_point_given_semicolon_separator():
    # Arrangement
    path = _creer_fichier_temporaire("1;2\n3;4\n5;6\n")

    # Action
    points = parse_points_file(path)
    os.unlink(path)

    # Assertion
    assert points[0] == (1.0, 2.0)


def test_should_parse_first_point_given_space_separator():
    # Arrangement
    path = _creer_fichier_temporaire("1 2\n3 4\n5 6\n")

    # Action
    points = parse_points_file(path)
    os.unlink(path)

    # Assertion
    assert points[0] == (1.0, 2.0)


# ── Contenu ignoré ────────────────────────────────────────────────────────────

def test_should_ignore_comments_and_blank_lines_given_mixed_content():
    # Arrangement
    path = _creer_fichier_temporaire("# commentaire\n\n1,2\n3,4\n5,6\n")

    # Action
    points = parse_points_file(path)
    os.unlink(path)

    # Assertion
    assert len(points) == 3


# ── Types numériques ──────────────────────────────────────────────────────────

def test_should_parse_float_values_given_decimal_coordinates():
    # Arrangement
    path = _creer_fichier_temporaire("1.5,2.7\n3.14,2.71\n0.0,0.0\n")

    # Action
    points = parse_points_file(path)
    os.unlink(path)

    # Assertion
    assert points[1] == (3.14, 2.71)


# ── Cas d'erreur ──────────────────────────────────────────────────────────────

def test_should_raise_value_error_given_less_than_three_points():
    # Arrangement
    path = _creer_fichier_temporaire("1,2\n3,4\n")

    # Action & Assertion
    with pytest.raises(ValueError, match="3 points"):
        parse_points_file(path)
    os.unlink(path)


def test_should_raise_value_error_given_three_values_on_one_line():
    # Arrangement
    path = _creer_fichier_temporaire("1,2,3\n4,5\n6,7\n")

    # Action & Assertion
    with pytest.raises(ValueError, match="format invalide"):
        parse_points_file(path)
    os.unlink(path)


def test_should_raise_value_error_given_non_numeric_values():
    # Arrangement
    path = _creer_fichier_temporaire("a,b\n1,2\n3,4\n")

    # Action & Assertion
    with pytest.raises(ValueError):
        parse_points_file(path)
    os.unlink(path)


def test_should_raise_file_not_found_given_missing_file():
    # Arrangement
    chemin_inexistant = "/chemin/inexistant/fichier.txt"

    # Action & Assertion
    with pytest.raises(FileNotFoundError):
        parse_points_file(chemin_inexistant)
