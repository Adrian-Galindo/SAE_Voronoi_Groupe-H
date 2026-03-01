"""Tests unitaires pour core/parser.py."""
import os
import tempfile

import pytest

from core.parser import parse_points_file


def _write_temp(content: str) -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return f.name


# ---------------------------------------------------------------------------
# Cas valides
# ---------------------------------------------------------------------------

def test_comma_separated():
    path = _write_temp("1,2\n3.5,4.0\n5,6\n")
    pts = parse_points_file(path)
    os.unlink(path)
    assert pts == [(1.0, 2.0), (3.5, 4.0), (5.0, 6.0)]


def test_semicolon_separated():
    path = _write_temp("1;2\n3;4\n5;6\n")
    pts = parse_points_file(path)
    os.unlink(path)
    assert pts[0] == (1.0, 2.0)


def test_space_separated():
    path = _write_temp("1 2\n3 4\n5 6\n")
    pts = parse_points_file(path)
    os.unlink(path)
    assert pts[0] == (1.0, 2.0)


def test_comments_and_blank_lines_ignored():
    content = "# commentaire\n\n1,2\n3,4\n5,6\n"
    path = _write_temp(content)
    pts = parse_points_file(path)
    os.unlink(path)
    assert len(pts) == 3


def test_float_coordinates():
    path = _write_temp("1.5,2.7\n3.14,2.71\n0.0,0.0\n")
    pts = parse_points_file(path)
    os.unlink(path)
    assert pts[1] == (3.14, 2.71)


# ---------------------------------------------------------------------------
# Cas d'erreur
# ---------------------------------------------------------------------------

def test_too_few_points_raises():
    path = _write_temp("1,2\n3,4\n")
    with pytest.raises(ValueError, match="3 points"):
        parse_points_file(path)
    os.unlink(path)


def test_invalid_format_raises():
    path = _write_temp("1,2,3\n4,5\n6,7\n")
    with pytest.raises(ValueError, match="format invalide"):
        parse_points_file(path)
    os.unlink(path)


def test_non_numeric_raises():
    path = _write_temp("a,b\n1,2\n3,4\n")
    with pytest.raises(ValueError):
        parse_points_file(path)
    os.unlink(path)


def test_file_not_found_raises():
    with pytest.raises(FileNotFoundError):
        parse_points_file("/chemin/inexistant/fichier.txt")
