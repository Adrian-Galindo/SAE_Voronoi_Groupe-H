import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import random


# -------------------------------------------------
# 1. Compute Voronoi
# -------------------------------------------------
def compute_voronoi(points):
    pts = np.array(points, dtype=float)

    if len(pts) < 3:
        raise ValueError("At least 3 points required for a bounded diagram")

    return Voronoi(pts)


# -------------------------------------------------
# 2. Convert infinite regions → finite polygons
# -------------------------------------------------
def voronoi_finite_polygons_2d(vor, radius=None):
    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)

    # Rayon dynamique calculé en fonction de l'espacement de tes points
    if radius is None:
        ptp_bound = np.ptp(vor.points, axis=0)
        radius = np.max(ptp_bound) * 10

    # Optimisation : dictionnaire pour trouver rapidement les arêtes
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    for p1, region_idx in enumerate(vor.point_region):
        vertices = vor.regions[region_idx]

        if all(v >= 0 for v in vertices):
            # Région déjà finie
            new_regions.append(vertices)
            continue

        ridges = all_ridges.get(p1, [])
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue

            # Calculer le point lointain pour fermer la région
            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # TRI DES SOMMETS : Indispensable pour éviter les polygones qui se croisent
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)].tolist()

        new_regions.append(new_region)

    return new_regions, np.asarray(new_vertices)


# -------------------------------------------------
# 3. Plot colored Voronoi
# -------------------------------------------------
def plot_voronoi_colored(vor):
    fig, ax = plt.subplots()

    regions, vertices = voronoi_finite_polygons_2d(vor)

    for region in regions:
        polygon = vertices[region]
        color = (
            random.random(),
            random.random(),
            random.random(),
        )
        ax.fill(*zip(*polygon), color=color, alpha=0.5)

    # Traits noirs
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(
                vor.vertices[simplex, 0],
                vor.vertices[simplex, 1],
                "k-",
                linewidth=1,
            )

    # Points (tes points d'entrée !)
    ax.plot(vor.points[:, 0], vor.points[:, 1], "ko")

    # CADRAGE (ZOOM) : Force le graphique à se concentrer sur tes points
    min_x, max_x = np.min(vor.points[:, 0]), np.max(vor.points[:, 0])
    min_y, max_y = np.min(vor.points[:, 1]), np.max(vor.points[:, 1])

    # On ajoute une marge de 10% autour des points
    dx = (max_x - min_x) * 0.1
    dy = (max_y - min_y) * 0.1

    ax.set_xlim(min_x - dx, max_x + dx)
    ax.set_ylim(min_y - dy, max_y + dy)

    ax.set_aspect("equal")
    ax.set_title("Voronoi Diagram Colored")

    return fig