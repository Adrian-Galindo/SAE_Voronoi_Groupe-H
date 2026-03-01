import { Delaunay } from "https://cdn.skypack.dev/d3-delaunay@6";

export default class VoronoiDiagram {
    constructor() {
        this.points = [];
        this.voro = null;
        this.colors = [];
    }

    compute(liste, w, h) {
        if (!liste || liste.length === 0) return;

        // inverser Y pour avoir 0 en bas
        const inverted = liste.map(p => ({ x: p.x, y: h - p.y }));

        this.points = inverted;

        const d = Delaunay.from(inverted, p => p.x, p => p.y);
        this.voro = d.voronoi([0, 0, w, h]);

        // Générer les couleurs UNE SEULE FOIS si nécessaire
        if (this.colors.length !== liste.length) {
            this.colors = liste.map(() => {
                const r = Math.floor(Math.random() * 255);
                const g = Math.floor(Math.random() * 255);
                const b = Math.floor(Math.random() * 255);
                return `rgb(${r},${g},${b})`;
            });
        }
    }

    draw(ctx) {
        if (!this.voro) return;

        for (let i = 0; i < this.points.length; i++) {
            ctx.beginPath();
            this.voro.renderCell(i, ctx);

            ctx.fillStyle = this.colors[i];
            ctx.fill();

            ctx.strokeStyle = "#000";
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }

        // Dessin des points
        ctx.fillStyle = "black";
        for (let p of this.points) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}