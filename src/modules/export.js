import { collectionPoints } from "./parsing.js";

document.getElementById("btn_export_png").addEventListener("click", exportCanvasPNG);
const message_export_error = document.getElementById("message_export_error");

export function exportCanvasPNG() {
    if (isCanvasEmpty()) {
        message_export_error.textContent = "Erreur : Le canvas est vide.";
        return;
    }

    const link = document.createElement("a");
    link.download = "voronoi.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
}

function isCanvasEmpty() {
    return collectionPoints.getPoints().length === 0;
}