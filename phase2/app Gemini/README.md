Générateur et Visualiseur de Diagramme de Voronoï 🕸️



Une application Python complète avec interface graphique permettant de générer, visualiser de manière interactive et exporter des diagrammes de Voronoï à partir d'un fichier de coordonnées.



📋 Fonctionnalités



Lecture robuste de fichiers texte contenant des paires de coordonnées X,Y.



Interface graphique intuitive (GUI) développée avec Tkinter.



Visualisation interactive via Matplotlib (Zoom in/out, déplacement (Pan), réinitialisation de la vue).



Exportation haute qualité dans différents formats : PNG, JPG et SVG (Vectoriel).



Code structuré, modulaire et vérifié par des tests unitaires automatisés.



🛠️ Prérequis et Installation



Assurez-vous d'avoir Python 3.8 ou supérieur installé sur votre système.

Téléchargez l'ensemble des fichiers du projet dans un même dossier.

Installez les dépendances requises via pip :

pip install -r requirements.txt



🚀 Utilisation

Pour lancer l'application, exécutez simplement le point d'entrée :

python main.py



Format du fichier texte attendu

Le fichier texte (.txt) doit contenir un point par ligne, séparé par une virgule. Les nombres décimaux doivent utiliser le point (.).
Exemple (fichier mes\_points.txt) :

12.5,4.2
3.1,8.9
15.0,15.0
0.5,2.3
7.7,7.7



(Remarque : L'algorithme nécessite un minimum de 4 points pour éviter les instabilités mathématiques sur des plans ouverts).



🧪 Exécution des Tests

Une suite de tests unitaires est incluse pour garantir la robustesse des opérations du noyau (lecture fichier et calcul mathématique). Pour lancer les tests :

python -m unittest test\_voronoi.py



🏛️ Architecture du Projet

main.py : Script de lancement principal.

voronoi\_gui.py : Classe gérant l'interface Tkinter et le pont avec Matplotlib.

voronoi\_core.py : Fonctions pures dédiées à la lecture des fichiers (I/O) et aux calculs géométriques (via SciPy).

test\_voronoi.py : Suite de tests unittest.

