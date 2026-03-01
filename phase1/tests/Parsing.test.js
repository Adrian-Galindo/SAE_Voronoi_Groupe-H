import { collectionPoints, setPointIntoCollection, clearCollection } from '../src/modules/parsing.js';

describe("Collection de points", () => {
    beforeEach(() => {
        // On crée un faux élément pour simuler la zone d'affichage
        const mockElement = { innerHTML: "" };
        clearCollection(mockElement);
    });

    test("Ajouter un point fonctionne", () => {
        setPointIntoCollection(1, 2);
        const points = collectionPoints.getPoints();
        expect(points.length).toBe(1);
        expect(points[0].x).toBe(1);
        expect(points[0].y).toBe(2);
    });

    test("Ajouter plusieurs points", () => {
        setPointIntoCollection(1, 2);
        setPointIntoCollection(3, 4);
        const points = collectionPoints.getPoints();
        expect(points.length).toBe(2);
    });
});