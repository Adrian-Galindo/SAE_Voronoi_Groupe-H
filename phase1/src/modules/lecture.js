import "./export.js"
import { getDessinVoronoi, clearCanva, resizeCanvas } from "./rendu.js";
import { clearCollection, collectionPoints, setPointIntoCollection, parseSaisieManuel, parseContenuFichier } from "./parsing.js";
import { validationFichier, validationCoordonneeRegex } from "../utils/validation.js";

let affichage_coordonnees = document.getElementById("affichage_coordonnees");

function createBaliseLiByPoint(x, y) {
    let li = document.createElement("li");
    li.textContent = `X: ${x}, Y: ${y}`;
    return li;
}

function lectureCoordonneesManuel() {
    let input_coordonnees_manuel = document.getElementById("coordonnees_manuel");
    let message_error_manuel = document.getElementById("message_error_saisie_manuel");
    let button_submit_coordonnees_manuel = document.getElementById("btn_submit_coordonnees_manuel");

    function resetInputSaisieManuel() {
        input_coordonnees_manuel.value = "";
        button_submit_coordonnees_manuel.disabled = true;
        message_error_manuel.textContent = "";
    }

    input_coordonnees_manuel.addEventListener("input", () => {
        let value = input_coordonnees_manuel.value.trim();
        if (value === "") {
            button_submit_coordonnees_manuel.disabled = true;
            message_error_manuel.textContent = "";
            return;
        }

        // Utilisation de la validation regex pour activer/désactiver le bouton
        const isValid = validationCoordonneeRegex(value);
        button_submit_coordonnees_manuel.disabled = !isValid;
        message_error_manuel.textContent = isValid ? "" : "Format invalide (X, Y).";
    });

    button_submit_coordonnees_manuel.addEventListener("click", () => {
        try {
            // ON UTILISE LA NOUVELLE FONCTION DE PARSING
            const points = parseSaisieManuel(input_coordonnees_manuel.value);

            points.forEach(p => {
                setPointIntoCollection(p.x, p.y);
                affichage_coordonnees.appendChild(createBaliseLiByPoint(p.x, p.y));
            });

            getDessinVoronoi();
            resetInputSaisieManuel();
        } catch (error) {
            message_error_manuel.textContent = error.message;
        }
    });
}

function lectureCoordonneesDrop() {
    const dropZone = document.getElementById("drop_zone");
    const fileInput = document.getElementById("file_input");
    const message_error_fichier = document.getElementById("message_error_fichier");

    dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("hover"); });
    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("hover"));
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("hover");
        handleFile(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener("change", (e) => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
            fileInput.value = "";
        }
    });

    function handleFile(file) {
        clearCollection(affichage_coordonnees);
        message_error_fichier.textContent = "";

        try {
            validationFichier(file);
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    // ON UTILISE LA NOUVELLE FONCTION DE PARSING
                    const points = parseContenuFichier(e.target.result);

                    points.forEach(p => {
                        setPointIntoCollection(p.x, p.y);
                        affichage_coordonnees.appendChild(createBaliseLiByPoint(p.x, p.y));
                    });

                    getDessinVoronoi();
                } catch (err) {
                    message_error_fichier.textContent = err.message;
                    clearCanva();
                }
            };
            reader.readAsText(file);
        } catch (error) {
            message_error_fichier.textContent = error.message;
        }
    }
}

function lectureResetPoint() {
    const btn_reset_points = document.getElementById("btn_reset_points");
    btn_reset_points.addEventListener("click", () => {
        if(collectionPoints.size() === 0) return; // S'il n'y a pas de points, on ne fait rien
        clearCollection(affichage_coordonnees);
        clearCanva();
    });
}

lectureCoordonneesManuel()

lectureCoordonneesDrop();

lectureResetPoint()

// Redraw uniquement quand l’utilisateur a fini de redimensionner.
let resizeTimeout;

window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        resizeCanvas();
    }, 150);
});

// Appel initial pour s'assurer que le canvas est à la bonne taille dès le départ
resizeCanvas();