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

## Scénario opérationnel
* Tablette : l'utilisateur peut demander (oral ou boutons) un objet spÃ©cifique et un rangement spÃ©cifique
* Aller jusqu'Ã  la table et prendre une photo
* Analyser la photo : rÃ©cupÃ©rer le nom des 3 objets et leur position
* Attraper le bon objet
* Le mettre dans le bon rangement

## Bonus 4 : Make a beautiful usecase
* Décor de chambre
* Rangement des 3 objets 
* IHR adapté : l'utilisateur sélectionne les objets à ranger là où il le souhaite. Si un objet (ou rangement) a déjà été sélectionné, il est directement remplacé par un objet (ou rangement) non utilisé.

## Tester notre code
Lancer dans chaque terminal les exports suivants :
* export PATH="/softwares/INFO/Pepper/python/python-2.7.16/bin":$PATH
* export PYTHONPATH=/softwares/INFO/Pepper/python/python-2.7.16/lib/python2.7/site-packages:${PYTHONPATH}
* export PYTHONPATH=${PYTHONPATH}:/softwares/INFO/Pepper/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

CHEMINS A CHANGER
* projet.py : putFile(chemin_photo/photo.png)
* projet.py : loadTopic(chemin_dialogue/dialogue_frf.top)

INSTALLER
* pip install opencv-python
* pip install algorithmia


