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

def handleState(currState):
    if currState == 0:
        px.forward(80)  # Idle driving
    elif currState == 1:
        currGray = px.get_grayscale_data()
        print(currGray)
        if sum(currGray) > 800:
            px.forward(0)
            px.stop
    elif currState == 2:
        print("Proceed with caution - Yield or duck detected")
        px.forward(0)
        # You can implement further logic to slow down or stop
    elif currState == 3:
        print("Turning left")
        px.forward(0)
        # Implement left turn logic
    elif currState == 4:
        print("Turning right")
        px.forward(0)
        # Implement right turn logic
    elif currState == 5:
        print("Going straight")
        px.forward(0)  # Go straight

    return currState
#Model
ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')

ROAD_SIGN_DETECTION_LABELS = path('labels.txt')

detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)
try:
    for frame in vision.get_frames():
        objects = detector.get_objects(frame, threshold=0.4)
        vision.draw_objects(frame, objects, labels)
        handleState(currState)
        if (objects):
            for thing in objects:
                #ducks in the road or yield sign, proceed with caution:
                if (thing.id == 0 or thing.id == 1 or thing.id == 6):
                    print("yield state")
                    #urrState = 2
                #stop sign detected
                if (thing.id == 2):
                    print("dis bish a stop sign please slip it in")
                    currState = 1
                #current_grayscale_value = px.get_grayscale_data()
            #handle states
finally:
    px.stop()
