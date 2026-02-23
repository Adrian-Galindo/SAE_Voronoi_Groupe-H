import VoronoiDiagram from "./voronoi.js";
import {collectionPoints} from "./parsing.js";

export const voronoi = new VoronoiDiagram()
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

export function clearCanva() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

export function getDessinVoronoi() {
    const points = collectionPoints.getPoints();

    message_export_error.textContent = ""; // on efface les messages d'erreur d'export à chaque nouveau dessin

    // Calcul
    voronoi.compute(points, canvas.width, canvas.height);
    // Dessin
    voronoi.draw(ctx);
}

export function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();

    canvas.width = rect.width;
    canvas.height = rect.height;

    // Redessiner après resize
    redraw();
}

function redraw() {
    const points = collectionPoints.getPoints();

    if (points.length === 0) return;

    clearCanva();

    voronoi.compute(points, canvas.width, canvas.height);
    voronoi.draw(ctx);
}