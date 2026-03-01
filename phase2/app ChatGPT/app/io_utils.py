from typing import List, Tuple


def read_points(file_path: str) -> List[Tuple[float, float]]:
    """Read points from a text file (format: x,y per line)."""
    points: List[Tuple[float, float]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            try:
                x_str, y_str = line.split(",")
                points.append((float(x_str), float(y_str)))
            except ValueError:
                raise ValueError(
                    f"Invalid format at line {line_number}: {line}"
                )

    if len(points) < 3:
        raise ValueError("At least 3 points required.")

    return points