from app.io_utils import read_points
from app.voronoi_engine import compute_voronoi
import tempfile


def test_full_pipeline():
    content = "0,0\n1,1\n2,0"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()

        pts = read_points(f.name)
        v = compute_voronoi(pts)

    assert v.points.shape[0] == 3
