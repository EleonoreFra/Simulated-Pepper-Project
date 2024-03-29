# Simulated-Pepper-Project

## Objectif
Simuler un robot Pepper qui detecte et range des objets dans des boites

## Auteurs
* Antoine REBOULLET
* Clément LECOCQ
* Eléonore FRANCOIS

## Vidéo youtube
Lien de la vidéo : [Cliquez-ici](https://www.youtube.com/watch?v=dzhw34h5zZk)

## Github 
https://github.com/EleonoreFra/Simulated-Pepper-Project/

## Sources
* http://doc.aldebaran.com/2-5/index_dev_guide.html
* https://algorithmia.com/algorithms/deeplearning/ObjectDetectionCOCO/docs
* https://gitlab.com/davidvivier/naoqi-tablet-simulator
* https://github.com/ProtolabSBRE/qibullet
* https://github.com/cpe-majeure-robotique/python_pepper_kinematics

## Projet initial commun
**Done** : 
Notre monde simulé comporte un décor et 3 objets montés sur un totem. L'ordre des objets sur la table est aléatoire.

Nous avons créé une IHR (Interface Homme Robot). L'utilisateur peut au début choisir (oralement ou avec les boutons) un objet spécifique et un rangement spécifique.

Le robot peut ensuite :
* Aller jusqu'à  la table et prendre une photo des 3 objets (vue d'ensemble)
* Analyser la photo : récupérer le nom des 3 objets et leur position associée
* Attraper le bon objet
* Le mettre dans le bon rangement associé

**Todo** :
* Améliorer la tablette : lorsque l'utilisateur clique un objet/rangement, supprimer l'option déjà choisie pour éviter d'effectuer deux fois le même choix.
* Ajouter des contraintes au robot : avec python_pepper_kinematics

**Bugs** :
Bonus : On ne peut pas attraper parfaitement les deux derniers objets. Nous avons alors passé beaucoup de temps là-dessus.


## Bonus
**Bonus 4 : Make a beautiful usecase**
Nous avons créé un scénario à notre simulation : le robot est chargé de ranger une chambre d'enfant. Voici nos améliorations :  
* Décor de chambre
* Rangement des 3 objets successifs  
Nous avons voulu réaliser un ensemble de 3 mouvements de façon successive. Pour ce faire, nous avons demandé au robot, après chaque saisie, de revenir à une position connue désignée comme origine. Cette position est aussi le point de départ et d'arrivée de tous les fonctions de rangement.
Un bruit a été ajouté au robot par les concepteurs de qibullet afin d'améliorer son réalisme, il a été par ce fait difficile de parvenir au résultat escompté et à ce que les 3 objets soient correctement attrapés. En effet, pour le dernier totem, le bruit s'étant ajouté à chaque mouvement précédent, le robot est donc pratiquement toujours en echec.
Ce travail nous a permis de toucher aux limites physiques du robot. Nous avons tenté, afin de palier ce problème, d'autres solutions comme la saisie à deux mains des objets mais elles se sont avérées moins efficaces.  
* IHR adapté : l'utilisateur sélectionne les objets à ranger là où il le souhaite. Si un objet (ou rangement) a déjà été sélectionné, il est directement remplacé par un objet (ou rangement) non utilisé.


## Comment tester notre code
1. Lancer dans chaque terminal les exports suivants :
* export PATH="/softwares/INFO/Pepper/python/python-2.7.16/bin":$PATH
* export PYTHONPATH=/softwares/INFO/Pepper/python/python-2.7.16/lib/python2.7/site-packages:${PYTHONPATH}
* export PYTHONPATH=${PYTHONPATH}:/softwares/INFO/Pepper/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages  


2. Changer les chemins suivants dans le code :
* projet.py : putFile(chemin_photo/photo.png)
* projet.py : loadTopic(chemin_dialogue/dialogue_frf.top)


