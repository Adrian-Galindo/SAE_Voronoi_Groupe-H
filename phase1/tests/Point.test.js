import Point from "../src/models/point.js";

describe("Classe Point", () => {

    test('Créer une instance de Point', () => {
        // Arrange & Act
        const p = new Point(10, 20);
        // Assert
        expect(p).toBeInstanceOf(Point);
    })

    test('Créer une instance de Point avec une seule coordonnée', () => {
        // Arrange & Act & Assert
        expect(()=>new Point(10)).toThrow("Point doit être initialisé avec des coordonnées x et y")
    })

    test("Création d\'un point avec des entiers positives", () => {
        // Arrange & Act
        const p = new Point(10, 20);
        // Assert
        expect(p.getX()).toBe(10);
        expect(p.getY()).toBe(20);
    });

    test("Création d\'un point avec des floats", () => {
        // Arrange & Act
        const p = new Point(3.5, 7.25);
        // Assert
        expect(p.getX()).toBe(3.5);
        expect(p.getY()).toBe(7.25);
    });

    test("Création d\'un point avec zéro", () => {
        // Arrange & Act
        const p = new Point(0, 0);
        // Assert
        expect(p.getX()).toBe(0);
        expect(p.getY()).toBe(0);

    });

    test('Création d\'un point avec des valeurs négatives', () => {
        // Arrange & Act & Assert
        expect(()=> new Point(-5, -10)).toThrow("X doit être un nombre entier");
    })

    test('Création d\'un point avec des valeurs non numériques', () => {
        // Arrange & Act & Assert
        expect(()=> new Point("a", "b")).toThrow("X doit être un nombre entier");
        expect(()=> new Point(null, null)).toThrow("X doit être un nombre entier");
    })

    test("setX, setY avec des valeurs non numériques", () => {
        // Arrange
        const p = new Point(10, 20);

        // Act & Assert
        expect(()=> p.setX("a")).toThrow("X doit être un nombre");
        expect(()=> p.setY("b")).toThrow("Y doit être un nombre");
    })

    test("setX, setY avec un nombre negative", () => {
        // Arrange
        const p = new Point(10, 20);

        // Act & Assert
        expect(()=> p.setX(-5)).toThrow("X doit être un nombre");
        expect(()=> p.setY(-5)).toThrow("Y doit être un nombre");
    });

    test("setX, setY avec un float", () => {
        // Arrange
        const p = new Point(10, 20);

        // Act & Assert
        expect(()=> p.setX(5.5)).not.toThrow("X doit être un nombre");
        expect(()=> p.setY(5.5)).not.toThrow("Y doit être un nombre");
    });

    test("setX, setY modifie correctement les valeurs", () => {
        const p = new Point(10, 20);

        p.setX(15.5);
        p.setY(25.5);

        expect(p.getX()).toBe(15.5);
        expect(p.getY()).toBe(25.5);
    });
});
