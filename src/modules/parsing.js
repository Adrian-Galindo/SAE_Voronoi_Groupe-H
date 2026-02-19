import Point from "../models/point.js";
import PointCollection from "../models/point_collection.js";

const collectionPoints = new PointCollection();

export function setPointIntoCollection(x, y) {
    let point = new Point(x,y);
    collectionPoints.addPoint(point);
}