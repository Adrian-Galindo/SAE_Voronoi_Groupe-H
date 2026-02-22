import Point from "../models/point.js";
import PointCollection from "../models/point_collection.js";

export const collectionPoints = new PointCollection();

export function setPointIntoCollection(x, y) {
    let point = new Point(x,y);
    collectionPoints.addPoint(point);
}

export function clearCollection(affichage_coordonnees){
    collectionPoints.clear();
    affichage_coordonnees.innerHTML = "";
}