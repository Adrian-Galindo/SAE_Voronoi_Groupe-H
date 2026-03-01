# diagramme_Voronoi
BUT-INFO | USPN | SAE S6 | 2026

## Description

Cette application web permet de générer et visualiser un **diagramme de Voronoï** à partir d’un ensemble de points du plan.

Les points peuvent être :

* Importés depuis un fichier contenant des coordonnées
* Saisis manuellement (un ou plusieurs points)
* Ajoutés dynamiquement dans l’interface

Le diagramme est calculé automatiquement et peut être exporté sous forme de **fichier SVG ou image (PNG)**.

---

# Objectifs

* Implémenter le calcul d’un diagramme de Voronoï
* Proposer une interface simple et conviviale
* Permettre plusieurs modes d’entrée des points
* Visualiser graphiquement le résultat
* Offrir une exportation du diagramme

---

# Choix de la solution

## Application Web

Nous avons choisi de développer une **application web** pour les raisons suivantes :

* Accessibilité sans installation
* Compatibilité multi-plateforme
* Affichage graphique interactif
* Support natif du format SVG
* Facilité d’export en image

---

# 🛠️ Technologies utilisées

* **HTML5** – Structure de l’interface
* **CSS3** – Mise en forme
* **JavaScript** – Logique et traitement
* **SVG** – Rendu vectoriel
* **d3-delaunay** – Génération du diagramme de Voronoï (bibliothèque D3 existante)
* **Jest** – Test unitaires

---

# Fonctionnalités

## Importation de fichier

L’utilisateur peut charger un fichier texte contenant des coordonnées sous la forme :

```
2,4
5.3,4.5
18,29
12.5,23.7
```

Chaque ligne correspond à un point :

```
x,y
```

### Traitement effectué :

* Lecture du fichier
* Analyse ligne par ligne
* Conversion en nombres réels
* Validation des coordonnées
* Stockage des points

---

## Saisie manuelle des points

L’application permet :

* L’ajout d’un point individuellement
* L’ajout de plusieurs points successivement
* La mise à jour automatique du diagramme après chaque ajout

---

## Calcul du diagramme

Le calcul repose sur les étapes suivantes :

1. Récupération des points
2. Génération de la triangulation de Delaunay
3. Construction du diagramme de Voronoï associé
4. Détermination des cellules et arêtes

Le calcul est automatiquement relancé à chaque modification des points. (réalisé par D3)

---

# Architecture

L’application est organisée en modules :

* **Lecture** : gestion de l’import des fichiers
* **Parsing** : transformation des données texte en coordonnées numériques
* **Calcul** : génération du diagramme de Voronoï
* **Rendu** : affichage du diagramme en SVG
* **Export** : génération des fichiers SVG ou PNG

---

# Flux de fonctionnement

1. L’utilisateur fournit des points (fichier ou saisie manuelle)
2. Les données sont validées et stockées
3. Le diagramme est calculé
4. Le résultat est affiché
5. L’utilisateur peut exporter le diagramme

---

# Perspectives d’amélioration

* Ajout du zoom et déplacement
* Suppression ou modification de points
* Coloration automatique des cellules
* Animation du processus de construction
* Affichage des coordonnées au survol

---

# Equipe

Projet réalisé par :
Adrian GALINDO
Bharani RATTINASSABABADY 
Mouhammed Diop
Anouar ROUIBI
Maxime LOINTIER
Huy PHAM

---
