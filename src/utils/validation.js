export function validationSaisiRegex(value) {
    // Expression régulière pour valider le format 'X, Y' (X et Y peuvent être des nombres avec des décimales)
    let regex = /^\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\s*$/;
    return value.match(regex);
}