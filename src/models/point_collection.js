const Point = require("./Point.js");

class PointCollection {
    constructor() {
        this.points = [];
    }

    addPoint(point) {
        if (!(point instanceof Point)) {
            throw new Error('Le point doit être une instance de la classe Point');
        }

        // Vérifie si un point avec les mêmes coordonnées existe déjà
        const exists = this.points.some(p => p.getX() === point.getX() && p.getY() === point.getY());
        if (exists) {
            throw new Error('Le point existe déjà dans la collection');
        }

        this.points.push(point);
    }

    getPoints() {
        return this.points;
    }

    removePointById(id) {
        if (typeof id !== 'number') {
            throw new Error('L\'ID doit être un nombre entier');
        }

        this.points = this.points.filter(p => p.id !== id);
    }

    clear() {
        this.points = [];
    }

    size() {
        return this.points.length;
    }

    toString() {
        if (this.points.length === 0) return "";
        return this.points.map(point => point.toString()).join(', ');
    }
}

module.exports = PointCollection;
