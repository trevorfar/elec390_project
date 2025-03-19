from aiymakerkit import vision
from aiymakerkit import utils
import cv2
import numpy as np
import time
from pycoral.utils.dataset import read_label_file
import os.path
from picarx import Picarx
px = Picarx()

#label_list = [
#0 duck_regular
#1 duck_specialty
#2 sign_stop
#3 sign_oneway_right
#4 sign_oneway_left
#5 sign_noentry
#6 sign_yield
#7 road_crosswalk
#8 road_oneway
#9 vehicle
#]


#States
#0 idle driving - scan for obstacles etc with camera
#1 stopping - brake lights on, scanning for white line to stop on
#2 caution - seeing yield sign - slow down and scan area
#3 turning left. Blinkers on, set steering angle
#4 turning right. Blinkers on set steering angle
#5 going straight. no blinkers, no steering angle
#6 seeing one way sign - scan area and continue with caution
currState = 0

def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)


#Model
ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')

ROAD_SIGN_DETECTION_LABELS = path('labels.txt')

detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)

for frame in vision.get_frames():
    objects = detector.get_objects(frame, threshold=0.4)
    vision.draw_objects(frame, objects, labels)
    def f(currState):
        match currState:
            case 0 :
                px.forward(80)
            case 1:
                currGray = px.get_greyscale_data()
                print(currGray)
                if(sum(currGray) == 1000):
                    px.forward(0)
                    currState = 5
                continue
                

    if (objects):
        for thing in objects
            #ducks in the road or yield sign, proceed with caution:
            if (thing.id == 0 OR thing.id == 1 OR thing.id == 6):
                print("yield state")
                currState = 2
            #stop sign detected
            if (thing.id == 2):
                print("dis bish a stop sign please slip it in")
                currState = 1
                #current_grayscale_value = px.get_grayscale_data()
    #handle states


    
