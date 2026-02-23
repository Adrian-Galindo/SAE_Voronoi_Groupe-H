export function validationCoordonneeRegex(value) {
    // Expression régulière pour valider le format 'X, Y' (X et Y peuvent être des nombres avec des décimales)
    // on peut ajouter plusieurs points séparés par un point-virgule si on veut (ex: "10,20; 30,40")
    let regex = /^\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\s*(;\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\s*)*;?\s*$/;
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