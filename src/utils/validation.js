export function validationCoordonneeRegex(value) {
    // Expression régulière pour valider le format 'X, Y' (X et Y peuvent être des nombres avec des décimales)
    let regex = /^\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\s*$/;
    return value.match(regex);
}

export function validationFichier(file) {
    if (!file) {
        throw Error("Aucun fichier sélectionné.")
    }

    if(file.type !== "text/plain") {
        throw Error("Format de fichier invalide. Veuillez sélectionner un fichier texte (.txt).");
    }
}