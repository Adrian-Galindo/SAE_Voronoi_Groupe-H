import "./export.js"
import {getDessinVoronoi,clearCanva, resizeCanvas} from "./rendu.js";
import {clearCollection, collectionPoints, setPointIntoCollection} from "./parsing.js";
import {validationFichier, validationCoordonneeRegex} from "../utils/validation.js";

let affichage_coordonnees = document.getElementById("affichage_coordonnees");

// Fonction pour créer un élément li pour afficher un point
function createBaliseLiByPoint(x, y) {
    let li = document.createElement("li");
    li.textContent = `X: ${x}, Y: ${y}`;
    return li;
}

function lectureCoordonneesManuel() {

    let input_coordonnees_manuel = document.getElementById("coordonnees_manuel");
    let message_error_manuel = document.getElementById("message_error_saisie_manuel");
    let button_submit_coordonnees_manuel = document.getElementById("btn_submit_coordonnees_manuel");

    // Fonction pour réinitialiser le champ et les messages
    function resetInputSaisieManuel() {
        input_coordonnees_manuel.value = "";
        button_submit_coordonnees_manuel.disabled = true;
        message_error_manuel.textContent = "";
    }

    // Écouteur d'événements pour l'entrée des coordonnées manuelles
    input_coordonnees_manuel.addEventListener("input", function(event) {
        let value = input_coordonnees_manuel.value;

        // Si l'entrée est vide, désactiver le bouton et réinitialiser les messages
        if(value.trim() === "") {
            button_submit_coordonnees_manuel.disabled = true;
            message_error_manuel.textContent = "";
            return;
        }

        let match = validationCoordonneeRegex(value);

        if (match) {
            // Activer le bouton de soumission si les coordonnées sont valides
            button_submit_coordonnees_manuel.disabled = false;

            // Réinitialiser les messages d'erreur
            message_error_manuel.textContent = "";
        } else {
            // Désactiver le bouton et réinitialiser l'affichage en cas d'erreur
            button_submit_coordonnees_manuel.disabled = true;
            message_error_manuel.textContent = "Format de coordonnées invalide. Veuillez entrer au format 'X, Y'.";
        }
    });

    // Permettre la soumission avec la touche "Entrée"
    input_coordonnees_manuel.addEventListener("keydown", function(event) {
        if (event.key === "Enter" && !button_submit_coordonnees_manuel.disabled) {
            event.preventDefault();
            button_submit_coordonnees_manuel.click();
        }
    });

    // Écouteur pour le bouton de soumission des coordonnées
    button_submit_coordonnees_manuel.addEventListener("click", function() {
        // On récupère la valeur saisie
        let value = input_coordonnees_manuel.value;

        // On vérifie le format global
        if (validationCoordonneeRegex(value)) {
            
            // Découpage de la chaine par les points virgules pour gérer plusieurs points à la fois
            let tableauPoints = value.split(';');

            try {
                //bouclage sur chaque coordonnée trouvée
                for(let i=0; i<tableauPoints.length; i++) {
                    let pointStr = tableauPoints[i].trim();
                    
                    // on resépare par la virgule pour avoir X et Y
                    let coord = pointStr.split(',');
                    
                    let pointX = parseFloat(coord[0]);
                    let pointY = parseFloat(coord[1]);

                    
                    setPointIntoCollection(pointX, pointY);

                    // Affichage dans la liste HTML
                    const li = createBaliseLiByPoint(pointX, pointY);
                    affichage_coordonnees.appendChild(li);
                }

                
                getDessinVoronoi();

                // vidage du champ
                resetInputSaisieManuel();

            } catch (error) {
                                
                message_error_manuel.textContent = 'Erreur lors de l\'ajout : ' + error.message;
            }

        } else {
            message_error_manuel.textContent = "Erreur : Format invalide.";
            clearCanva();
        }
    });
}

function lectureCoordonneesDrop() {
    const dropZone = document.getElementById("drop_zone");
    const fileInput = document.getElementById("file_input");
    const message_error_fichier = document.getElementById("message_error_fichier");

    // --- Hover pour le drag ---
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("hover");
    });

    dropZone.addEventListener("dragleave", (e) => {
        dropZone.classList.remove("hover");
    });

    // --- Drop ---
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("hover");
        handleFile(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener("change", (e) => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
            fileInput.value = ""; // reset pour pouvoir recharger le même fichier
        }
    });

    // --- Fonction centrale pour traiter un fichier ---
    function handleFile(file) {
        // Réinitialiser l'affichage et les messages d'erreur
        clearCollection(affichage_coordonnees);
        message_error_fichier.textContent = "";

        if (!file) return;

        try {
            validationFichier(file);
        } catch (error) {
            message_error_fichier.textContent = error.message;
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const contenu = e.target.result;
            traiterContenuFichier(contenu);
        };
        reader.onerror = () => {
            message_error_fichier.textContent = "Erreur lors de la lecture du fichier.";
        };
        reader.readAsText(file);
    }

    // --- Fonction qui parse le contenu (ton code actuel) ---
    function traiterContenuFichier(contenu) {
        try {
            const lignes = contenu.split("\n");
            lignes.forEach((ligne, index) => {
                const trimmed = ligne.trim();
                if (trimmed === "") throw Error("Le fichier contient des lignes vides.");

                const parties = trimmed.split(",");
                const match = validationCoordonneeRegex(trimmed);
                if (!match) throw Error(`ligne ${index + 1} : format invalide`);

                const x = parseFloat(parties[0]);
                const y = parseFloat(parties[1]);

                setPointIntoCollection(x, y);

                const li = createBaliseLiByPoint(x, y);
                affichage_coordonnees.appendChild(li);
            });

            getDessinVoronoi();
        } catch (error) {
            message_error_fichier.textContent = `Erreur dans le fichier : ${error.message}`;
            clearCollection(affichage_coordonnees);
            clearCanva();
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