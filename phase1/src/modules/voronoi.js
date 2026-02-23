import { Delaunay } from "https://cdn.skypack.dev/d3-delaunay@6";

// voronoï - coloré selon position
export default class VoronoiDiagram {
    constructor() {
        this.points = [];
        this.voro = null;
    }

    compute(liste, w, h) {
        if (!liste || liste.length === 0) return; // juste au cas ou ça plante
        this.points = liste;

        const d = Delaunay.from(liste, p => p.x, p => p.y);
        this.voro = d.voronoi([0, 0, w, h]);
    }

    draw(ctx) {
        if (!this.voro) return;

        for (let i = 0; i < this.points.length; i++) {
            const p = this.points[i];
            ctx.beginPath();
            this.voro.renderCell(i, ctx);

            // couleur aléatoire à chaque fois, ça sera plus funky
            // Je prends des nombres random entre 0 et 255
            const r = Math.floor(Math.random() * 255);
            const g = Math.floor(Math.random() * 255);
            const b = Math.floor(Math.random() * 255);
            
            ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
            ctx.fill();

            ctx.strokeStyle = "#000";
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }

        // les points
        ctx.fillStyle = "black";
        for (let p of this.points) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2); // *2 ou 2* c'est pareil
            ctx.fill();
        }
        
    }
}