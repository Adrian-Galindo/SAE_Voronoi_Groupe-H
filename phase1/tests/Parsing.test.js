import { collectionPoints, setPointIntoCollection, clearCollection, parseSaisieManuel, parseContenuFichier } from '../src/modules/parsing.js';

describe("Parsing test", () => {
    beforeEach(() => {
        // On crée un faux élément pour simuler la zone d'affichage
        const mockElement = { innerHTML: "" };
        clearCollection(mockElement);
    });

    test("Ajouter un point fonctionne", () => {
        // Arrange & Act
        setPointIntoCollection(1, 2);
        const points = collectionPoints.getPoints();
        // Assert
        expect(points.length).toBe(1);
        expect(points[0].x).toBe(1);
        expect(points[0].y).toBe(2);
    });

    test("Ajouter plusieurs points", () => {
        // Arrange & Act
        setPointIntoCollection(1, 2);
        setPointIntoCollection(3, 4);
        const points = collectionPoints.getPoints();
        // Assert
        expect(points.length).toBe(2);
    });

    test("Vider la collection", () => {
        // Arrange & Act
        setPointIntoCollection(1, 2);
        const points = collectionPoints.getPoints();
        const mockElement = { innerHTML: "" };
        // Act
        clearCollection(mockElement);
        // Assert
        expect(collectionPoints.getPoints().length).toBe(0);
    });

    test("Ajouter des valeurs invalides leve exception", () => {
        // Arrange & Act & Assert
        expect(() => setPointIntoCollection("a", "b")).toThrow();
        expect(() => setPointIntoCollection(null, null)).toThrow();
        expect(() => setPointIntoCollection(undefined, undefined)).toThrow();
    })

    test("Ajouter des valeurs limites", () => {
        // Arrange & Act
        setPointIntoCollection(Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER);
        const points = collectionPoints.getPoints();
        // Assert
        expect(points.length).toBe(1);
        expect(points[0].x).toBe(Number.MAX_SAFE_INTEGER);
        expect(points[0].y).toBe(Number.MAX_SAFE_INTEGER);
    })

    test("Ajouter des valeurs négatives leve Exception", () => {
        // Arrange & Act & Assert
        expect(() => setPointIntoCollection(-1, -1)).toThrow();
    })

    test("Parsing de saisie manuel valide", () => {
        // Arrange
        const input = "1,2; 3,4; 5,6";
        // Act
        const points = parseSaisieManuel(input);
        // Assert
        expect(points.length).toBe(3);
        expect(points[0]).toEqual({ x: 1, y: 2 });
        expect(points[1]).toEqual({ x: 3, y: 4 });
        expect(points[2]).toEqual({ x: 5, y: 6 });
    })

    test("Parsing de saisie manuel invalide leve exception", () => {
        // Arrange
        const input = "1,2; invalid; 5,6";
        // Act & Assert
        expect(() => parseSaisieManuel(input)).toThrow("Format de coordonnées invalide.");
    })

    test("Parsing de contenu de fichier valide", () => {
        // Arrange
        const contenu = "1,2\n3,4\n5,6";
        // Act
        const points = parseContenuFichier(contenu);
        // Assert
        expect(points.length).toBe(3);
        expect(points[0]).toEqual({ x: 1, y: 2 });
        expect(points[1]).toEqual({ x: 3, y: 4 });
        expect(points[2]).toEqual({ x: 5, y: 6 });
    })

    test("Parsing de contenu de fichier invalide leve exception", () => {
        // Arrange
        const contenu = "1,2\ninvalid\n5,6";
        // Act & Assert
        expect(() => parseContenuFichier(contenu)).toThrow("ligne 2 : format invalide");
    })

    test("Parsing de contenu de fichier vide leve exception", () => {
        // Arrange
        const contenu = "";
        // Act & Assert
        expect(() => parseContenuFichier(contenu)).toThrow("Le fichier est vide.");
    })

    test("Parsing de contenu de fichier avec des lignes vides", () => {
        // Arrange
        const contenu = "1,2\n\n3,4\n\n5,6";
        // Act
        const points = parseContenuFichier(contenu);
        // Assert
        expect(points.length).toBe(3);
        expect(points[0]).toEqual({ x: 1, y: 2 });
        expect(points[1]).toEqual({ x: 3, y: 4 });
        expect(points[2]).toEqual({ x: 5, y: 6 });
    })

    test("Parsing de contenu de fichier avec des espaces", () => {
        // Arrange
        const contenu = " 1,2 \n 3,4 \n 5,6 ";
        // Act
        const points = parseContenuFichier(contenu);
        // Assert
        expect(points.length).toBe(3);
        expect(points[0]).toEqual({ x: 1, y: 2 });
        expect(points[1]).toEqual({ x: 3, y: 4 });
        expect(points[2]).toEqual({ x: 5, y: 6 });
    })

    test("Parsing de contenu de fichier avec des string non numériques leve exception", () => {
        // Arrange
        const contenu = "1,2\nabc,def\n5,6";
        // Act & Assert
        expect(() => parseContenuFichier(contenu)).toThrow("ligne 2 : format invalide");
    })
});