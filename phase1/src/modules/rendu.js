import { collectionPoints } from "./parsing.js";
import VoronoiDiagram from "./voronoi.js";

// instance du Voronoi
export const voronoi = new VoronoiDiagram();

// récupération du canvas et contexte
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// --- Fonction pour vider le canvas ---
export function clearCanva() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// --- Fonction pour normaliser les points selon la taille du canvas ---
export function normalizePoints(points, canvas, padding = 40) {
    if (!points || points.length === 0) return [];

    const xs = points.map(p => p.x);
    const ys = points.map(p => p.y);

    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    const rangeX = maxX - minX || 1; // éviter division par 0
    const rangeY = maxY - minY || 1;

    return points.map(p => ({
        x: padding + ((p.x - minX) / rangeX) * (canvas.width - padding * 2),
        y: padding + ((p.y - minY) / rangeY) * (canvas.height - padding * 2)
    }));
}

// --- Fonction principale pour dessiner le Voronoï ---
export function getDessinVoronoi() {
    const rawPoints = collectionPoints.getPoints();
    if (rawPoints.length === 0) return;

    // réinitialiser le message d'erreur d'export
    const message_export_error = document.getElementById("message_export_error");
    message_export_error.textContent = "";

    // normalisation des points
    const normalizedPoints = normalizePoints(rawPoints, canvas, 40);

    // calcul et dessin
    voronoi.compute(normalizedPoints, canvas.width, canvas.height);
    voronoi.draw(ctx);
}

// --- Fonction pour redimensionner le canvas ---
export function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    // redraw après resize
    redraw();
}

// --- Redraw : recalculer et dessiner le Voronoï ---
function redraw() {
    const rawPoints = collectionPoints.getPoints();
    if (rawPoints.length === 0) return;

    clearCanva();

    const normalizedPoints = normalizePoints(rawPoints, canvas, 40);

    voronoi.compute(normalizedPoints, canvas.width, canvas.height);
    voronoi.draw(ctx);
}