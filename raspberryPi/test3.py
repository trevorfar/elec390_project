from picarx import Picarx
from enum import Enum
import time
from aiymakerkit import vision
from aiymakerkit import utils
import cv2
import numpy as np
from pycoral.utils.dataset import read_label_file
import os.path
from robot_hat import Pin
import time

leftSignal = Pin('D0')
rightSignal = Pin('D1')

# leftTurn = Pin('P8')
# rightTurn = Pin('P9')
#forwardLights.value(1)
         
def turnSignal(direction, num):
    for i in range(num):
        direction.value(1)
        time.sleep(0.1)
        direction.value(0)
        time.sleep(0.1)


px = Picarx()
instructions = []
with open("instructions.txt", "r") as file:
    for line in file:
        instruction = line.strip()
        if instruction:
            instructions.append(instruction)
print(instructions)

speed = 1
drift = 1
yielding = 0

def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)

ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')
ROAD_SIGN_DETECTION_LABELS = path('labels.txt')
detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)

class Label(Enum):
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
    
    
class State(Enum):
    idle_driving = 0
    stopping = 1
    stopped = 2
    turn_right = 3
    turn_left = 4
    big_right = 5
    big_left = 6
    drift = 7
    
currState = State.idle_driving
def Encoder(instructions):
     global currState
     print(instructions)
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
     elif(instructions == "x"):
         time.sleep(5)
         instructions.pop(0)
         currState = State.idle_driving



def move(x):
     #px.set_dir_servo_angle(-2)
     px.set_motor_speed(1, x)
     px.set_motor_speed(2, -x)
     
     
def turn(turn_radius, length, direction):
    global currState
    
    px.set_dir_servo_angle(turn_radius)
    move(speed)
    #led on
    #time.sleep(length/4)
    #led off
    #time.sleep(length/4)
    #led on
    #time.sleep(length/4)
    #led off
    #time.sleep(length/4)
    #led
    direction.value(1)
    time.sleep(length/6)
    direction.value(0)
    time.sleep(length/6)
    direction.value(1)
    time.sleep(length/6)
    direction.value(0)
    time.sleep(length/6)
    direction.value(1)
    time.sleep(length/6)
    direction.value(0)
    time.sleep(length/6)
    #time.sleep(length)
    print("we boutta go driving")
    print(turn_radius)
    currState = State.idle_driving

def handle_state():
    global currState
    global yielding
    global stopLights
    global drift
    
    if(currState == State.idle_driving):
        print("idle driving")
        adjust_direction()
        move(speed)
        
        currState = State.stopping # COMMENT OUT AFTER
        
    elif(currState == State.stopping):
        print("stopping")
        adjust_direction()
        leftSignal.value(1)
        rightSignal.value(1)
        currGray = px.get_grayscale_data()
        if ((currGray[0] > 300 and currGray[1] > 300 and currGray[2] > 300)):
            move(0)
            
            if(yielding):
                time.sleep(1)
                yielding = 0
            else:
                time.sleep(2.5)
            leftSignal.value(0)
            rightSignal.value(0)
            currState = State.stopped
#192.168.1.13
    elif(currState == State.stopped):
        print("stopped")
        if(drift and instructions[0] == "go"):
            currState = State.drift
            drift = 0
        else:
            Encoder(instructions[0])
        instructions.pop(0)
    
        
    elif(currState == State.turn_right):
        px.set_dir_servo_angle(-3)
        move(1)
        time.sleep(0.5)
        #turnSignal(rightSignal, 5)
        print("right")
        turn(30, 2, rightSignal)
    elif(currState == State.turn_left):
        px.set_dir_servo_angle(-3)
        move(1)
        time.sleep(0.5)

       # turnSignal(leftSignal, 5)
        print("left")
        turn(-20, 3, leftSignal)
    elif(currState == State.big_right):
        print("big right")
        turn(20, 3)
    elif(currState == State.big_left):
        print("big_left")
        turn(20, 3)
    elif(currState == State.drift):
        print("drift")
        px.set_dir_servo_angle(-3)
        move(speed) # adjust 
        time.sleep(2) # adjust 
        px.set_motor_speed(1, 100)
        px.set_motor_speed(2, 100)
        time.sleep(8) # adjust, (time a full rotation)
        currState = State.idle_driving

def adjust_direction():
    global yielding 
    sensor_values = px.get_grayscale_data()

    left_sensor = sensor_values[0]
    right_sensor = sensor_values[2]

    if left_sensor > 300:
        px.set_dir_servo_angle(30)  
    elif right_sensor > 300:
        px.set_dir_servo_angle(-30) 
    else:
        px.set_dir_servo_angle(-3)
        
        
        
# while True:
#     handle_state()
    

try:
     for frame in vision.get_frames():
         objects = detector.get_objects(frame, threshold=0.4)
         vision.draw_objects(frame, objects, labels)
         handle_state()
         if (objects):
             for item in objects:
                 if (item.id == Label.duck_regular or item.id == Label.sign_yield):
                     print("yield")
                     yielding = 1
                     currState = State.yielding
                 if (item.id == Label.sign_stop):
                     print("stop")
                     currState = State.stopping
finally:
     px.stop()





        



