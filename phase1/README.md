# Diagramme Voronoi
BUT-INFO | USPN | SAE S6 | 2026

## Description

Cette application web permet de générer et visualiser un **diagramme de Voronoï** à partir d’un ensemble de points du plan.

Les points peuvent être :

* Importés depuis un fichier contenant des coordonnées
* Saisis manuellement (un ou plusieurs points)

Le diagramme est calculé automatiquement et peut être exporté sous forme de **image (PNG)**.

---

# Technologies utilisées

* **HTML5** – Structure de l’interface
* **CSS3** – Mise en forme
* **JavaScript** – Logique et traitement
* **d3-delaunay** – Génération du diagramme de Voronoï (bibliothèque D3 existante)
* **Jest** – Test unitaires

---

# Visualisation

* Le diagramme s’affiche automatiquement.
* Il s’adapte à la taille de la fenêtre.
* Un bouton permet de réinitialiser les points.

---

# Fonctionnalités

## Importation de fichier ou glisser

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

## Saisie manuelle des points

L’application permet :

* L’ajout d’un point individuellement
* L’ajout de plusieurs points successivement
* La mise à jour automatique du diagramme après chaque ajout

---

# Architecture

L’application est organisée en modules :

* **Lecture** : gestion de l’import des fichiers
* **Parsing** : transformation des données texte en coordonnées numériques
* **Vonoroi** : génération du diagramme de Voronoï
* **Rendu** : affichage du diagramme
* **Export** : génération des fichiers PNG

---

# Equipe

Projet réalisé par :
* Adrian GALINDO
* Bharani RATTINASSABABADY 
* Mouhammed Diop
* Anouar ROUIBI
* Maxime LOINTIER
* Huy PHAM
