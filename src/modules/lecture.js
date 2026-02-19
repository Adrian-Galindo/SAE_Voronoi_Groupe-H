import {setPointIntoCollection} from "./parsing.js";
import {validationSaisiRegex} from "../utils/validation.js";

// Fonction pour créer un élément li pour afficher un point
function createBaliseLiByPoint(x, y) {
    let li = document.createElement("li");
    li.textContent = `X: ${x}, Y: ${y}`;
    return li;
}

// Fonction pour réinitialiser le champ et les messages
function resetInputSaisieManuel() {
    input_coordonnees_manuel.value = "";
    button_submit_coordonnees_manuel.disabled = true;
    message_error_manuel.textContent = "";
}

function lectureCoordonneesManuel() {

    let input_coordonnees_manuel = document.getElementById("coordonnees_manuel");
    let message_error_manuel = document.getElementById("message_error_saisie_manuel");
    let affichage_coordonnees_manuel = document.getElementById("affichage_coordonnees_manuel");
    let button_submit_coordonnees_manuel = document.getElementById("btn_submit_coordonnees_manuel");

    // Écouteur d'événements pour l'entrée des coordonnées manuelles
    input_coordonnees_manuel.addEventListener("input", function(event) {
        let value = input_coordonnees_manuel.value;

        // Si l'entrée est vide, désactiver le bouton et réinitialiser les messages
        if(value.trim() === "") {
            button_submit_coordonnees_manuel.disabled = true;
            message_error_manuel.textContent = "";
            return;
        }

        let match = validationSaisiRegex(value);

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

        let match = validationSaisiRegex(value);

        if (match) {
            let pointX = parseFloat(match[1]);
            let pointY = parseFloat(match[3]);

            try{
                // Ajouter le point à la collection de points
                setPointIntoCollection(pointX, pointY);

                // Créer un élément <li> pour afficher le point
                const li = createBaliseLiByPoint(pointX, pointY);
                affichage_coordonnees_manuel.appendChild(li);

                // Réinitialiser le champ et désactiver le bouton
                resetInputSaisieManuel();
            }
            catch (error) {
                // Réinitialiser le champ et désactiver le bouton
                resetInputSaisieManuel();

                // Afficher une erreur si l'ajout du point échoue (par exemple, si les coordonnées sont hors limites)
                message_error_manuel.textContent = 'Erreur : ' + error.message;
            }

        } else {
            // Afficher une erreur si le format est incorrect (bien que ce cas soit déjà géré en amont)
            message_error_manuel.textContent = "Erreur : Coordonnées invalides.";
        }
    });

}

function lectureCoordonneesFichier() {

}

lectureCoordonneesManuel()