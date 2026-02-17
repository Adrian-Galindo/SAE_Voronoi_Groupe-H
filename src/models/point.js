class Point {
    static id = 1;

    constructor(x, y) {
        this.setX(x);
        this.setY(y);
        this.id = Point.id++;
    }

    setX(x) {
        if (x < 0 || typeof x !== "number") {
            throw new Error('X doit être un nombre entier');
        }
        this.x = x;
    }

    setY(y) {
        if (y < 0 || typeof y !== "number") {
            throw new Error('Y doit être un nombre entier');
        }
        this.y = y;
    }

    getX() {
        return this.x;
    }

    getY() {
        return this.y;
    }

    toString() {
        return `(${this.x}, ${this.y})`;
    }
}

module.exports = Point;
