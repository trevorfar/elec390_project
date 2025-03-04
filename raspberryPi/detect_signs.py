from aiymakerkit import vision
from aiymakerkit import utils
from pycoral.utils.dataset import read_label_file

import os.path

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


def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)

#Model
ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')

#Lables
ROAD_SIGN_DETECTION_LABELS = path('labels.txt')

detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)
for frame in vision.get_frames():
    objects = detector.get_objects(frame, threshold=0.4)
    vision.draw_objects(frame, objects, labels)
    if (objects):
        if (objects[0].id == 2):
            print("dis bish a stop sign please slip it in")
        elif (objects[0].id == 6):
            print("dis a yield sign, DO NOT SLIP IT IN")
        elif (objects[0].id == 0):
            print("dis a mf duck, *smirks*")
