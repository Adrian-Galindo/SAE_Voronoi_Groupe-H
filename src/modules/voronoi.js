// Gère le calcul et l'affichage Voronoi ( pas de biblio externe D3)

class VoronoiDiagram {
    constructor() {
        this.donnees = []; // On stocke les points ici
    }

    // juste pour récupérer les données, le calcul se fait direct dans le draw
    compute(listePoints, w, h) {
        this.donnees = listePoints;
    }

    // Affiche le résultat dans le canvas
    // J'utilise l'algo naif qui regarde pixel par pixel
    draw(contexte, zoneDessin) {
        const largeur = zoneDessin.width;
        const hauteur = zoneDessin.height;
        
        // On récupère le tableau de pixels pour écrire dedans directement
        const pixels = contexte.createImageData(largeur, hauteur);
        const data = pixels.data;

        // On scanne toute l'image
        for (let x = 0; x < largeur; x++) {
            for (let y = 0; y < hauteur; y++) {
                
                let distanceMin = 999999999; // une valeur très grande au départ
                let pointGagnant = -1; // l'index du point le plus proche

                // Pour chaque pixel, on regarde quel est le point de référence le plus près
                for (let i = 0; i < this.donnees.length; i++) {
                    const p = this.donnees[i];
                    
                    // calcul de distance classique (Pythagore)
                    // astuce vue sur starckoverflow pour le perf du cpu
                    const dx = x - p.x;
                    const dy = y - p.y;
                    const d = (dx * dx) + (dy * dy);
                    
                    if (d < distanceMin) {
                        distanceMin = d;
                        pointGagnant = i;
                    }
                }

                // le pixel actuel dans le tableau (y * largeur + x) * 4 canaux (r,g,b,a)
                const indexPixel = (y * largeur + x) * 4;
                
                // J'utilise l'index du point gagnant pour faire une couleur unique
                // C'est du bricolage avec des nombres premiers pour que les couleurs soient différentes
                data[indexPixel] = (pointGagnant * 123) % 255;      // Rouge
                data[indexPixel + 1] = (pointGagnant * 321) % 255;  // Vert
                data[indexPixel + 2] = (pointGagnant * 213) % 255;  // Bleu
                data[indexPixel + 3] = 255;                         // Alpha (opaque)
            }
        }

        // On remet l'image calculée dans le canvas
        contexte.putImageData(pixels, 0, 0);

        // On redessine les points noirs par-dessus pour bien voir les centres
        contexte.fillStyle = "black";
        for (const pt of this.donnees) {
            contexte.beginPath();
            contexte.arc(pt.x, pt.y, 3, 0, 2 * Math.PI);
            contexte.fill();
        }
    }
}

module.exports = VoronoiDiagram;
