const PointCollection = require('./models/point_collection.js');
const Point = require('./models/Point.js');

describe('Classe PointCollection', () => {
    let collection;
    let p1, p2;

    beforeEach(() => {
        collection = new PointCollection();
        p1 = new Point(10, 20);
        p2 = new Point(30, 40);
    });

    test('Créer une instance de PointCollection', () => {
        // Act & Assert
        expect(collection).toBeInstanceOf(PointCollection);
        expect(collection.size()).toBe(0);
    });

    test("Ajouter un point unique fonctionne", () => {
        // Act
        collection.addPoint(p1);
        // Assert
        expect(collection.size()).toBe(1);
        expect(collection.getPoints()).toContain(p1);
    });

    test("Ajouter un point qui n'est pas un Point lève une erreur", () => {
        // Act & Assert
        expect(() => collection.addPoint({x: 10, y: 20})).toThrow('Le point doit être une instance de la classe Point');
    });

    test("Ajouter un point identique lève une erreur", () => {
        // Arrange
        const duplicate = new Point(10, 20); // même x et y
        // Act
        collection.addPoint(p1);
        // Assert
        expect(() => collection.addPoint(duplicate)).toThrow('Le point existe déjà dans la collection');
    });

    test("Ajouter un point différent fonctionne", () => {
        // Act
        collection.addPoint(p1);
        collection.addPoint(p2);
        // Assert
        expect(collection.size()).toBe(2);
        expect(collection.getPoints()).toEqual([p1, p2]);
    });

    test("Obtenir tous les points de la collection", () => {
        // Act
        collection.addPoint(p1);
        collection.addPoint(p2);
        const points = collection.getPoints();
        // Assert
        expect(points).toEqual(expect.arrayContaining([p1, p2]));
    });

    test("Supprimer un point par son ID", () => {
        // Act
        collection.addPoint(p1);
        collection.addPoint(p2);
        collection.removePointById(p1.id);
        // Assert
        expect(collection.getPoints()).not.toContain(p1);
        expect(collection.getPoints()).toContain(p2);
        expect(collection.size()).toBe(1);
    });

    test("Supprimer un point inexistant ne plante pas", () => {
        // Act
        collection.addPoint(p1);
        // Assert
        expect(() => collection.removePointById(999)).not.toThrow();
        expect(collection.size()).toBe(1);
    });

    test("Supprimer avec un ID non numérique (string) lève une erreur", () => {
        // Act & Assert
        expect(() => collection.removePointById("a")).toThrow("L'ID doit être un nombre entier");
    });

    test("Supprimer avec un ID non numérique (null) lève une erreur", () => {
        // Act & Assert
        expect(() => collection.removePointById(null)).toThrow("L'ID doit être un nombre entier");
    })

    test("Vider la collection de points", () => {
        collection.addPoint(p1);
        collection.addPoint(p2);
        collection.clear();
        expect(collection.getPoints()).toEqual([]);
        expect(collection.size()).toBe(0);
    });

    test("Obtenir la taille de la collection", () => {
        collection.addPoint(p1);
        collection.addPoint(p2);
        expect(collection.size()).toBe(2);
    });

    test("clear() sur une collection vide ne plante pas", () => {
        expect(() => collection.clear()).not.toThrow();
        expect(collection.size()).toBe(0);
    });

    test("toString() sur une collection non vide", () => {
        collection.addPoint(p1);
        collection.addPoint(p2);
        expect(collection.toString()).toBe(`${p1.toString()}, ${p2.toString()}`);
    });

    test("toString() sur une collection vide", () => {
        expect(collection.toString()).toBe("");
    });
});
