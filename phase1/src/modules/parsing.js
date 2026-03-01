import Point from "../models/point.js";
import PointCollection from "../models/point_collection.js";
import { validationCoordonneeRegex } from "../utils/validation.js";

export const collectionPoints = new PointCollection();

export function setPointIntoCollection(x, y) {
    let point = new Point(x,y);
    collectionPoints.addPoint(point);
}

export function clearCollection(affichage_coordonnees){
    collectionPoints.clear();
    affichage_coordonnees.innerHTML = "";
}

// Logique de parsing pure pour la saisie manuelle
export function parseSaisieManuel(valeur) {
    if (!validationCoordonneeRegex(valeur)) {
        throw new Error("Format de coordonnées invalide.");
    }

    return valeur.split(';').map(pointStr => {
        const coord = pointStr.trim().split(',');
        return {
            x: parseFloat(coord[0]),
            y: parseFloat(coord[1])
        };
    });
}

// Logique de parsing pure pour le contenu d'un fichier
export function parseContenuFichier(contenu) {
    const lignes = contenu.split("\n").filter(l => l.trim() !== "");
    if (lignes.length === 0) throw new Error("Le fichier est vide.");

    return lignes.map((ligne, index) => {
        const trimmed = ligne.trim();
        if (!validationCoordonneeRegex(trimmed)) {
            throw new Error(`ligne ${index + 1} : format invalide`);
        }
        const parties = trimmed.split(",");
        return {
            x: parseFloat(parties[0]),
            y: parseFloat(parties[1])
        };
    });
}