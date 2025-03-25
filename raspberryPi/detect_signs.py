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
def move():
    px.set_motor_speed(1, 1)
    px.set_motor_speed(2, -1)
def turnSmallLeft():
    px.set_dir_servo_angle(30)
    px.move()
    time.sleep(0.5)
    
def turnSmallRight():
    px.set_dir_servo_angle(-30)
    px.move()
    time.sleep(2)
    
def turnBigLeft():
    print("sex")
def turnBigRight():
    print("sex")
def checkStop():
    sensor_values = px.get_grayscale_data()
    currGray = sensor_values
    move()
    time.sleep(1)
    currState =0;
    if ((currGray[0]>200 and currGray[1]>200 and currGray[2]>200) and currState == 0):
            px.forward(0)
            print("stopped")
            time.sleep(2)
            currState = 2
def adjust_direction():
    """Adjust the car's direction based on grayscale sensor values."""
    sensor_values = px.get_grayscale_data()
    move()
    #currState =0;
    left_sensor = sensor_values[0]
    right_sensor = sensor_values[2]
    if(currState == 2):
        turnSmallRight()
        
    if left_sensor > 200:
        print("Left sensor detected high value! Turning right.")
        px.set_dir_servo_angle(30)  
    elif right_sensor > 200:
        print("Right sensor detected high value! Turning left.")
        px.set_dir_servo_angle(-30)  
    
    else:
        px.set_dir_servo_angle(-2)

def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)

def handleState():
    global currState
    
    if currState == 0:
        px.forward(10)  # Idle driving
    elif currState == 1:
        currGray = px.get_grayscale_data()
        print(currGray)
        if ((currGray[0]>800 and currGray[1]>800) or (currGray[0]>800 and currGray[2]>800) or (currGray[1]>800 and currGray[2]>800)):
            px.forward(0)
            print("stopped")
            time.sleep(5)
            currState =5
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
        px.forward(10)  # Go straight
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
        handleState()
        adjust_direction()
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
