"""Tests unitaires — export/svg_exporter.py et export/image_exporter.py."""
import os
import tempfile

from matplotlib.figure import Figure

from export.svg_exporter import export_svg
from export.image_exporter import export_image


def _creer_figure_test() -> Figure:
    """Construit une figure Matplotlib simple pour les tests d'export."""
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot([0, 1, 2], [0, 1, 0])
    return fig


# ── Export SVG ────────────────────────────────────────────────────────────────

def test_should_create_svg_file_given_valid_figure():
    # Arrangement
    figure = _creer_figure_test()
    chemin = tempfile.mktemp(suffix=".svg")

    # Action
    export_svg(figure, chemin)

    # Assertion
    assert os.path.exists(chemin)
    assert os.path.getsize(chemin) > 0
    os.unlink(chemin)


def test_should_write_svg_markup_given_matplotlib_figure():
    # Arrangement
    figure = _creer_figure_test()
    chemin = tempfile.mktemp(suffix=".svg")

    # Action
    export_svg(figure, chemin)

    # Assertion
    with open(chemin, encoding="utf-8") as fh:
        contenu = fh.read()
    assert "<svg" in contenu
    os.unlink(chemin)


# ── Export PNG ────────────────────────────────────────────────────────────────

def test_should_create_png_file_given_valid_figure():
    # Arrangement
    figure = _creer_figure_test()
    chemin = tempfile.mktemp(suffix=".png")

    # Action
    export_image(figure, chemin)

    # Assertion
    assert os.path.exists(chemin)
    assert os.path.getsize(chemin) > 0
    os.unlink(chemin)


# ── Export JPG ────────────────────────────────────────────────────────────────

def test_should_create_jpg_file_given_jpeg_extension():
    # Arrangement
    figure = _creer_figure_test()
    chemin = tempfile.mktemp(suffix=".jpg")

    # Action
    export_image(figure, chemin)

    # Assertion
    assert os.path.exists(chemin)
    assert os.path.getsize(chemin) > 0
    os.unlink(chemin)
