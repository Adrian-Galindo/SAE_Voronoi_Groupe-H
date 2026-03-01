from app.io_utils import read_points
import tempfile


def test_read_points_valid():
    content = "1,2\n3,4"
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        pts = read_points(f.name)

    assert pts == [(1.0, 2.0), (3.0, 4.0)]
