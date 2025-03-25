from picarx import Picarx
from enum import Enum
import time
from aiymakerkit import vision
from aiymakerkit import utils
import cv2
import numpy as np
from pycoral.utils.dataset import read_label_file
import os.path

px = Picarx()
instructions = ["turn_left", "turn_right", "big_right", "big_left", "go"]
speed = 1
drift = 1
ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')
ROAD_SIGN_DETECTION_LABELS = path('labels.txt')
detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)

class Label(enum)
    duck_regular = 0
    duck_specialty = 1
    sign_stop = 2
    sign_oneway_right = 3
    sign_oneway_left = 4
    sign_noentry = 5
    sign_yield = 6
    road_crosswalk = 7
    road_oneway = 8
    vehicle = 9
    
print(Label.vehicle)
    
class State(enum):
    idle_driving = 0
    stopping = 1
    stopped = 2
    turn_right = 3
    turn_left = 4
    big_right = 5
    big_left = 6
    drift = 7

def Encoder(instructions):
     if(instructions == "turn_left"):
         currState = State.turn_left
     elif(instructions == "turn_right"):
         currState = State.turn_right
     elif(instructions == "big_left"):
         currState = State.big_left
     elif(instructions == "big_right"):
         currState = State.big_right
     elif(instructions == "go"):
         currState = State.idle_driving
         
def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)

currState = State.idle_driving


def move(x):
     px.set_motor_speed(1, x)
     px.set_motor_speed(2, -x)
     
def turn(turn_radius, length):
    px.set_dir_servo_angle(turn_radius)
    move(speed)
    time.sleep(length)
    currState = State.idle_driving

def handle_state():
    global currState
    if(currState == State.idle_driving):
        adjust_direction()
        move(speed)
    elif(currState == State.stopping):
        currGray = px.get_grayscale_data()
        if ((currGray[0] > 300 and currGray[1] > 300 and currGray[2] > 300)):
            move(0)
            time.sleep(2.5)
            currState = State.stopped

    elif(currState == State.stopped):
        if(drift and instructions[0] == "go")
            currState = State.drift
            drift = 0
        else:
            Encoder(instructions[0])
        instructions.pop(0)
    elif(currState == State.turn_right):
        turn(30, 2)
    elif(currState == State.turn_left):
        turn(-30, 2)
    elif(currState == State.big_right):
        turn(20, 3)
    elif(currState == State.big_left):
        turn(20, 3)
    elif(currState == State.drift):
        move(speed) # adjust 
        time.sleep(2) # adjust 
        px.set_motor_speed(1, 70)
        px.set_motor_speed(2, 70)
        time.sleep(2) # adjust, (time a full rotation)
        currState = State.idle_driving

def adjust_direction():
    """Adjust the car's direction based on grayscale sensor values."""    
    sensor_values = px.get_grayscale_data()

    left_sensor = sensor_values[0]
    right_sensor = sensor_values[2]

    if left_sensor > 200:
        print("Left sensor detected high value! Turning right.")
        px.set_dir_servo_angle(30)  # Adjust the angle as needed
    elif right_sensor > 200:
        print("Right sensor detected high value! Turning left.")
        px.set_dir_servo_angle(-30)  # Adjust the angle as needed
    else:
        px.set_dir_servo_angle(0)
        
try:
    for frame in vision.get_frames():
        objects = detector.get_objects(frame, threshold=0.4)
        vision.draw_objects(frame, objects, labels)
        handle_state()
        if (objects):
            for item in objects:
                if (item.id == Label.duck_regular or item.id == Label.sign_yield):
                    print("yield")
                if (item.id == Label.sign_stop):
                    print("stop")
                    currState = State.stopping
finally:
    px.stop()





        

