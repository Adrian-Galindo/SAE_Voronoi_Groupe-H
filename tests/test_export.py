"""Tests unitaires pour export/svg_exporter.py et export/image_exporter.py."""
import os
import tempfile

import pytest
from matplotlib.figure import Figure

from export.svg_exporter import export_svg
from export.image_exporter import export_image


def _make_figure() -> Figure:
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot([0, 1, 2], [0, 1, 0])
    return fig


# ---------------------------------------------------------------------------
# Export SVG
# ---------------------------------------------------------------------------

def test_export_svg_creates_file():
    fig = _make_figure()
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
        path = f.name
    try:
        export_svg(fig, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0
    finally:
        os.unlink(path)


def test_export_svg_valid_content():
    fig = _make_figure()
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False, mode="w") as f:
        path = f.name
    try:
        export_svg(fig, path)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "<svg" in content
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Export PNG
# ---------------------------------------------------------------------------

def test_export_png_creates_file():
    fig = _make_figure()
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = f.name
    try:
        export_image(fig, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Export JPG
# ---------------------------------------------------------------------------

def test_export_jpg_creates_file():
    fig = _make_figure()
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        path = f.name
    try:
        export_image(fig, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0
    finally:
        os.unlink(path)
