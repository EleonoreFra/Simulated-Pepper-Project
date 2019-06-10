# Simulated-Pepper-Project

## Projet
Robot qui range une chambre

## Auteurs
* Antoine REBOULLET
* Clément LECOCQ
* Eléonore FRANCOIS

## Vidéo
Lien de la vidéo : [Cliquez-ici](https://www.youtube.com/watch?v=dzhw34h5zZk)

## Sources
* http://doc.aldebaran.com/2-5/index_dev_guide.html
* https://algorithmia.com/algorithms/deeplearning/ObjectDetectionCOCO/docs
* https://gitlab.com/davidvivier/naoqi-tablet-simulator
* https://github.com/ProtolabSBRE/qibullet
* https://github.com/cpe-majeure-robotique/python_pepper_kinematics

## Fonctionnalités
* IHR : d'abord, l'utilisateur peut choisir (oralement ou avec les boutons) un objet spécifique et un rangement spécifique
* Aller jusqu'à  la table et prendre une photo
* Analyser la photo : récupérer le nom des 3 objets et leur position associée
* Attraper le bon objet
* Le mettre dans le bon rangement

## Bonus 4 : Make a beautiful usecase
* Décor de chambre
* Rangement des 3 objets 
* IHR adapté : l'utilisateur sélectionne les objets à ranger là où il le souhaite. Si un objet (ou rangement) a déjà été sélectionné, il est directement remplacé par un objet (ou rangement) non utilisé.
Presque opérationnel : le robot a du mal a attraper parfaitement les deux derniers objets

## Tester notre code
1. Lancer dans chaque terminal les exports suivants :
* export PATH="/softwares/INFO/Pepper/python/python-2.7.16/bin":$PATH
* export PYTHONPATH=/softwares/INFO/Pepper/python/python-2.7.16/lib/python2.7/site-packages:${PYTHONPATH}
* export PYTHONPATH=${PYTHONPATH}:/softwares/INFO/Pepper/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

2. Changer les chemins suivants dans le code :
* projet.py : putFile(chemin_photo/photo.png)
* projet.py : loadTopic(chemin_dialogue/dialogue_frf.top)


