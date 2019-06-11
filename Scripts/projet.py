#!/usr/bin/env python
# coding: utf-8

import Algorithmia
from Algorithmia.acl import ReadAcl, AclType
import cv2
import time
from qibullet import SimulationManager
from qibullet import PepperVirtual
import pybullet
import pybullet_data
import random
from qibullet.camera import *
import qi
import argparse
import sys
import signal

global x1,x2,x3
global asked_object
global asked_rangement

def gene_positions(liste):
    """
    Give a random position for each object
    """
    global x1,x2,x3
    x1 = random.choice(liste)
    liste.remove(x1)
    x2 = random.choice(liste)
    liste.remove(x2)
    x3 = random.choice(liste)
    liste.remove(x3)

def init_decor(client):
    """
    Creation of the different elements in the environment
    """
    global x1,x2,x3
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath()) 
   
    pybullet.loadURDF(
        "/decor/table/table.urdf",
        basePosition=[3, 0, 0.30],
        globalScaling=10.0,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "/decor/ball/totemball.urdf",
        basePosition=[2.7, x1, 0.65],
        physicsClientId=client)
    
    pybullet.loadURDF(
        "/decor/teddy/totemteddybear.urdf",
        basePosition=[2.7, x2, 0.65],
        physicsClientId=client)
    
    pybullet.loadURDF(
        "/decor/bird/totembird.urdf",
        basePosition=[2.7, x3, 0.65],
        physicsClientId=client)

    pybullet.loadURDF(
        "/decor/bed/bed.urdf",
        basePosition=[0.3, -2.9, 1],
        physicsClientId=client)

    pybullet.loadURDF(
        "/decor/box/box.urdf",
        basePosition=[0.5, 0.5, 0.19],
        physicsClientId=client)
    
    pybullet.loadURDF(
        "/decor/chair/chair.urdf",
        basePosition=[3, -2, 0.3],
        physicsClientId=client)

    pybullet.loadURDF(
        "/decor/night/night.urdf",
        basePosition=[0, -2, 0.2],
        physicsClientId=client)

    pybullet.loadURDF(
        "/decor/floor/floor.urdf",
        basePosition=[3, 0, 0.01],
        globalScaling=10.0,
        physicsClientId=client)

def init_posture(pepper):
    """
    Give the original posture of Pepper
    """
    pepper.goToPosture("Crouch", 0.6)
    time.sleep(1)
    pepper.goToPosture("Stand", 0.6)
    time.sleep(1)
    pepper.goToPosture("LyingBack", 0.6)
    time.sleep(1)

def get_image(pepper):
    """ 
    Get Frame and save it
    """
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM, resolution=Camera.K_VGA) # Enable the camera (we change the resolution)
    img = pepper.getCameraFrame() # Take a picture
    cv2.imshow("bottom camera", img)
    cv2.waitKey(2000) # Wait 2s before close the frame
    cv2.imwrite("photo.png",img) # Save the image
    cv2.destroyAllWindows() # Close the frame
    pepper.unsubscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)


def analyse_image(client):
    """
    Analyze the picture and give the objects on it with their position
    1 : the object is on the right (trough the robot view)
    2 : middle
    3 : left
    """
    # Cle client
    apiKey = "sim7EmBW6yOYvc88W9F/V3oUfAu1"

    # Create the Algorithmia client
    client = Algorithmia.client(apiKey)

    # Set your Data URI
    nlp_directory = client.dir("data://antoine_rb/nlp_directory")

    # Create your data collection if it does not exist
    if nlp_directory.exists() is False:
        nlp_directory.create()

    # Create the acl object and check if it's the .my_algos default setting
    acl = nlp_directory.get_permissions()  # Acl object
    acl.read_acl == AclType.my_algos  # True

    # Update permissions to private
    nlp_directory.update_permissions(ReadAcl.private)
    nlp_directory.get_permissions().read_acl == AclType.private # True

    img_file = "data://antoine_rb/nlp_directory/photo.png"

    # Upload local file CHANGER LE CHEMIN
    client.file(img_file).putFile("/home/tp/softbankRobotics/apps/FRANCOIS_LECOCQ_REBOULLET_BONUS_4/Scripts/photo.png")

    input = {
      "image": "data://antoine_rb/nlp_directory/photo.png",
      "output": "data://.algo/deeplearning/ObjectDetectionCOCO/temp/imgout.jpg",
      "min_score": 0.4,
      "model": "ssd_mobilenet_v1"
    }

    # Create the algorithm object using the Summarizer algorithm
    algo = client.algo("deeplearning/ObjectDetectionCOCO/0.2.1")

    
    dico_objets = {}

    # Pass in input required by algorithm
    try:
	# Give the result of the analyse
        output = algo.pipe(input).result
        dico = output['boxes']
        print(dico)

	    # Give a list of the 3 objects
        obj1 = dico[0]['label']
        obj2 = dico[1]['label']
        obj3 = dico[2]['label']
        list_objets = [obj1, obj2, obj3] 
        
        # Give the positions of each object 
        # 1 for left, 2 middle, 3 right
        i = 0
        for objet in list_objets:
            dic_coord = dico[i]['coordinates']
            center = (dic_coord['x0'] + dic_coord['x1']) / 2
            if (1 < center < 200):
                dico_objets[objet] = 3  # Objet à gauche
            elif(201 < center < 380):
                dico_objets[objet] = 2  # Objet au milieu
            elif(381 < center < 600):
                dico_objets[objet] = 1  # Objet à droite
            i += 1
        print(dico_objets)

    except Exception as error:
        # Algorithm error if, for example, the input is not correctly formatted
        print(error)

    return(dico_objets)

def grab_object(pepper,numero_obj):
    """
    Take the object in the hand
    """   
    pepper.moveTo(0.31,0,0) # avancer un peu vers la table
    move_Obj(pepper,numero_obj) # se décaler vers le totem, prendre en compte la position de la table
    pepper.setAngles('RElbowYaw',1.4,0.5) 
    pepper.setAngles('RShoulderPitch',0.82,0.25) 
    time.sleep(1)
    pepper.setAngles('RHand',6,0.5) # ouvrir la main
    time.sleep(0.5)
    pepper.moveTo(0.18,0,0)
    time.sleep(0.5)
    pepper.moveTo(0,0.05,0)
    time.sleep(1)
    pepper.moveTo(0.05,0,0)
    pepper.setAngles('RHand',0,0.2)
    time.sleep(0.5)
    pepper.setAngles('RShoulderPitch',0.4,0.1)
    recentrer(pepper,numero_obj)
    time.sleep(1)
    
def move_Obj(pepper,numero_obj):
    """
    Place the robot in front of the right object 
    """
    # Object on the right
    if numero_obj == 1:
        pepper.moveTo(0,-0.1,0)

    # Object on the middle
    if numero_obj == 2:
        pepper.moveTo(0,0.13,0)

    # Object on the left
    if numero_obj == 3:
        pepper.moveTo(0,0.33,0)
    
def recentrer(pepper,numero_obj):
    """
    Replace the robot at a known position
    """
    if numero_obj == 1:
        pepper.moveTo(-0.54,0,0)
        time.sleep(0.5)
        pepper.moveTo(0,0.04,0)
    if numero_obj == 2:
        pepper.moveTo(-0.54,0,0)
        time.sleep(0.5)
        pepper.moveTo(0,-0.17,0)
    if numero_obj == 3:
        pepper.moveTo(-0.54,0,0)
        time.sleep(0.5)
        pepper.moveTo(0,-0.38,0)

def drop_carton(pepper):
    """
    Move to the carton and drop the object in it
    """
    pepper.moveTo(-1.3,0,0)
    time.sleep(0.5)
    pepper.moveTo(0,0,1.47)
    pepper.setAngles('RElbowYaw',-1,0.5)
    pepper.setAngles('RHand',6,1)
    time.sleep(0.5)
    pepper.setAngles('RElbowYaw',1.2,0.5)
    pepper.setAngles('RElbowRoll',0.5,0.5)
    pepper.setAngles('RShoulderPitch',1.58,0.5)
    pepper.setAngles('RHand',1,1)
    pepper.moveTo(0,0,-1.47)
    time.sleep(0.5)
    pepper.moveTo(1.3,0,0)
    time.sleep(1)

def drop_night(pepper):
    """
    Move to the night table and drop the object on it
    """
    pepper.setAngles('RShoulderPitch',0,0.1)
    pepper.setAngles('RElbowYaw',1.6,0.1)
    pepper.setAngles('RElbowRoll',0,0.1)
    pepper.moveTo(-1.9,-1.6,-1.5708)
    time.sleep(1)
    pepper.setAngles('RWristYaw',-0.3,0.1)
    pepper.setAngles('RShoulderPitch',0.1,0.1)
    pepper.setAngles('RHand',6,0.1)
    time.sleep(2)
    pepper.setAngles('RShoulderPitch',-1,0.1)
    pepper.moveTo(-0.9,0,-3.1415)
    time.sleep(0.5)
    pepper.setAngles('RElbowYaw',1.2,0.5)
    pepper.setAngles('RElbowRoll',0.5,0.5)
    pepper.setAngles('RShoulderPitch',1.58,0.5)
    pepper.setAngles('RHand',1,1)
    pepper.setAngles('RWristYaw',0,0.1)
    pepper.moveTo(0.7,-1.9,-1.5708)
    time.sleep(1)

def drop_chair(pepper):
    """
    Move to the chair and drop the object on it
    """
    pepper.setAngles('RShoulderPitch',0,0.1)
    pepper.setAngles('RElbowYaw',1.6,0.1)
    pepper.setAngles('RElbowRoll',0,0.1)
    pepper.moveTo(0,-1.4,0)
    time.sleep(1)
    pepper.setAngles('RShoulderRoll',-4,0.1)
    time.sleep(1)
    pepper.moveTo(1.2,0,0)
    pepper.setAngles('RWristYaw',-0.3,0.1)
    pepper.setAngles('RHand',6,0.7)
    time.sleep(1)
    pepper.moveTo(-1.2,0,0)
    pepper.setAngles('RElbowYaw',1.2,0.5)
    pepper.setAngles('RElbowRoll',0.5,0.5)
    pepper.setAngles('RShoulderPitch',1.58,0.5)
    pepper.setAngles('RHand',1,1)
    pepper.setAngles('RWristYaw',0,0.1)
    pepper.setAngles('RShoulderRoll',0,0.1)
    pepper.moveTo(0,1.4,0)
    time.sleep(1)


def dab(pepper):
    """
    Show that it is the end of the process
    """
    pepper.setAngles('RShoulderRoll',-4,0.4)
    pepper.setAngles('RElbowRoll',0,0.4)
    pepper.setAngles('RHand',0.9,0.4)
    pepper.setAngles('RShoulderPitch',0.7,0.4)
    pepper.setAngles('LWristYaw',-0.6,0.4)
    pepper.setAngles('LShoulderPitch',0.08,0.4)
    pepper.setAngles('LHand',1.1,0.4)
    pepper.setAngles('LShoulderRoll',0.15,0.4)
    pepper.setAngles('LElbowYaw',-0.3,0.4)
    time.sleep(0.3)
    pepper.setAngles('LElbowRoll',-1.35,0.4)
    pepper.setAngles('HeadPitch',0.5,0.1)

def association_object(value):
    """
    Store the asked object
    """
    global asked_object
    print "val:", value
    asked_object = value
    

def association_rangement(value):
    """
    Store the asked rangement
    """
    global asked_rangement
    print "val:", value
    asked_rangement = value

def user_request(session):
    """
    Give the user request (one object and one rangement)
    """
    global asked_object
    global asked_rangement

    liste_asked_object = []
    liste_asked_rangement = []
    liste_three_objects = ["teddy bear","sports ball","bird"]
    liste_three_rangements = ["table","carton","fauteuil"]
    
    # Get the service ALTabletService.
    try:
        tabletService = session.service("ALTabletService")
        tabletService.loadApplication("FRANCOIS_LECOCQ_REBOULLET_BONUS_4/Scripts")
        tabletService.showWebview()

    except Exception, e:
        print "Error was: ", e


    # Service ALMemory (pour récupérer des variables du js)
    try:
        memoryService = session.service("ALMemory")

    except Exception, e:
        print "Error was: ", e

    # Getting the service ALDialog
    try:
    	ALDialog = session.service("ALDialog")
        ALDialog.resetAll()
    	ALDialog.setLanguage("French")

    	# Loading the topics directly as text strings
    	topic_name = ALDialog.loadTopic("/home/tp/softbankRobotics/apps/FRANCOIS_LECOCQ_REBOULLET_BONUS_4/Scripts/dialogue_frf.top")

    	# Activating the loaded topics
    	ALDialog.activateTopic(topic_name)

    	# Starting the dialog engine - we need to type an arbitrary string as the identifier
    	# We subscribe only ONCE, regardless of the number of topics we have activated
    	ALDialog.subscribe('dialogue')

    except Exception, e:
        print "Error was: ", e

    try:
        for i in range(3):
            memoryService.insertData("Objet", 0)
	
            sub = memoryService.subscriber("Objet")
            sub.signal.connect(association_object) 
	
            while(memoryService.getData("Objet") == 0):
                time.sleep(1)

            if asked_object in liste_asked_object:
                if asked_object in liste_three_objects:
                    liste_three_objects.remove(asked_object)
                liste_asked_object.append(liste_three_objects[0])
                liste_three_objects.remove(liste_three_objects[0])
            else:
                liste_asked_object.append(asked_object)

            time.sleep(3)

            memoryService.insertData("Rangement", 0)

            sub = memoryService.subscriber("Rangement")
            sub.signal.connect(association_rangement)

            while(memoryService.getData("Rangement") == 0):
                time.sleep(1)
	
            if asked_rangement in liste_asked_rangement:
                if asked_rangement in liste_three_rangements:
                    liste_three_rangements.remove(asked_rangement)
                liste_asked_rangement.append(liste_three_rangements[0])
                liste_three_rangements.remove(liste_three_rangements[0])
            else:
                liste_asked_rangement.append(asked_rangement)

	        time.sleep(3)


        print(liste_asked_object)
        print(liste_asked_rangement)

        return(liste_asked_rangement,liste_asked_object)

    except Exception, e:
        print "Error was: ", e


def main(session):
    global asked_object
    global asked_rangement

    # Create the simulation with the Pepper
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    # Original positions of the objects (give random positions)
    liste = [-0.2,0,0.2] 
    gene_positions(liste)

    # Initialization of the decor and the robot
    init_decor(client)
    init_posture(pepper)
    
    # The user asks an object and a rangement
    [liste_asked_rangement,liste_asked_object] = user_request(session)

    # Step 1 : Detect the 3 objects and their position
    pepper.moveTo(1.9,0,0) # Move to the position to take the picture
    get_image(pepper) 
    dico_objets = analyse_image(client)

    for i in range(len(liste_asked_rangement)):
        numero_obj = dico_objets[liste_asked_object[i]] # Give the position of the object asked 
        
        # Step 2 : Take the object asked
        grab_object(pepper,numero_obj)

        # Step 3 : Store the object in the right place
        if (liste_asked_rangement[i] == "table"):
            drop_night(pepper)
        elif (liste_asked_rangement[i] == "fauteuil"):
            drop_chair(pepper)
        elif (liste_asked_rangement[i] == "carton"):
            drop_carton(pepper)

    # Step 4 : DAB
    dab(pepper)

    while True:
	    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()

    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))

    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
