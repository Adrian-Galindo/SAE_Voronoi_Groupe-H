import "./export.js"
import {getDessinVoronoi,clearCanva} from "./rendu.js";
import {clearCollection, setPointIntoCollection} from "./parsing.js";
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

    // Écouteur pour le bouton de soumission des coordonnées
    button_submit_coordonnees_manuel.addEventListener("click", function() {
        // On fait a nouveau une validation pour s'assurer que les coordonnées sont correctes avant de les afficher (possible manipulation de l'utilisateur)
        let value = input_coordonnees_manuel.value;

        let match = validationCoordonneeRegex(value);

        if (match) {
            let pointX = parseFloat(match[1]);
            let pointY = parseFloat(match[3]);

            try{
                // Ajouter le point à la collection de points
                setPointIntoCollection(pointX, pointY);

                // Mettre à jour le dessin du diagramme de Voronoï
                getDessinVoronoi()

                // Créer un élément <li> pour afficher le point
                const li = createBaliseLiByPoint(pointX, pointY);
                affichage_coordonnees.appendChild(li);

                // Réinitialiser le champ et désactiver le bouton
                resetInputSaisieManuel();
            }
            catch (error) {
                // Réinitialiser le champ et désactiver le bouton
                resetInputSaisieManuel();
                clearCanva()

                // Afficher une erreur si l'ajout du point échoue (par exemple, si les coordonnées sont hors limites)
                message_error_manuel.textContent = 'Erreur : ' + error.message;
            }

        } else {
            // Afficher une erreur si le format est incorrect (bien que ce cas soit déjà géré en amont)
            message_error_manuel.textContent = "Erreur : Coordonnées invalides.";
            clearCanva()
        }
    });

}

function lectureCoordonneesFichier() {

    let input_fichier_coordonnees = document.getElementById("coordonnees_fichier");
    let message_error_fichier = document.getElementById("message_error_fichier");

    function traiterContenuFichier(contenu) {
        message_error_fichier.textContent = "";

        try{
            const lignes = contenu.split("\n");

            lignes.forEach((ligne, index) => {
                const trimmed = ligne.trim();

                if (trimmed === "") throw Error("Le fichier contient des lignes vides.");

                const parties = trimmed.split(",");

                let match = validationCoordonneeRegex(trimmed);

                if (!match) {
                    throw Error(`ligne ${index + 1} : format invalide`);
                }

                const x = parseFloat(parties[0]);
                const y = parseFloat(parties[1]);

                setPointIntoCollection(x, y);

                const li = createBaliseLiByPoint(x, y);
                affichage_coordonnees.appendChild(li);
            });

            // Mettre à jour le dessin du diagramme de Voronoï
            getDessinVoronoi()
        }
        catch (error) {
            message_error_fichier.textContent = `Erreur dans le fichier : ${error.message}`;
            clearCollection(affichage_coordonnees)
            clearCanva()
        }
    }

    function handleFile(event) {
        // Avant de traiter un nouveau fichier, on réinitialise la collection de points et l'affichage
        clearCollection(affichage_coordonnees)

        const file = event.target.files[0];

        try{
            validationFichier(file)
        }catch (error) {
            message_error_fichier.textContent = error.message;
            return;
        }

        const reader = new FileReader();

        reader.onload = function(e) {
            const contenu = e.target.result;
            traiterContenuFichier(contenu);
        };

        reader.onerror = function() {
            message_error_fichier.textContent = "Erreur lors de la lecture du fichier.";
        };

        reader.readAsText(file);
    }

    input_fichier_coordonnees.addEventListener("change", handleFile);

}

lectureCoordonneesManuel()

lectureCoordonneesFichier()