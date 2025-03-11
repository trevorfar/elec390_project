from aiymakerkit import vision
from aiymakerkit import utils
import cv2
import numpy as np
import time

from pycoral.utils.dataset import read_label_file
from picarx import Picarx
# bunk i was doing from trevorTesting import filterAndModel
import time
    
import os.path

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


#STates
#0 idle driving - scan for obstacles etc with camera
#1 stopping - brake lights on, scanning for white line to stop on
#turning and shit
#seeing yield / one way signs


def path(name):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, 'models', name)


#chatgpt ass code so if it doesnt work or interferes, or is unnecessary delete that shit asap
def whiteBalanceBullshit(img):
    result = img.copy()
    meanBlue = np.mean(img[:, :, 0])
    meanGreen = np.mean(img[:, :, 1])
    meanRed = np.mean(img[:, :, 2])
    
    scaleBlue = meanGreen/meanBlue
    scaleRed = meanGreen/meanBlue
    
    result[:, :, 0] = np.clip(img[:, :, 0] * scaleBlue, 0, 255)
    result[:, :, 2] = np.clip(img[:, :, 2] * scaleRed, 0, 255)
    return result.astype(np.uint8)


def process_image(img, height, width):
    # HSV color ranges for lane detection
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 60, 255])
    
    # Region of interest (ROI)
    roi_top = 0.6  
    roi_bottom = 1.0
    
    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # Combine masks
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)
    
    # Create ROI mask
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[
        (0, int(height * roi_top)), 
        (width, int(height * roi_top)), 
        (width, height), 
        (0, height)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, roi_vertices, 255)
    roi = cv2.bitwise_and(combined, mask)
    
    # Edge detection
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    return edges

#Model
ROAD_SIGN_DETECTION_MODEL = path('efficientdet-lite.tflite')
ROAD_SIGN_DETECTION_MODEL_EDGETPU = path('efficientdet-lite_edgetpu.tflite')
#a = [1,2, 4]
#print(a)
#Lables
ROAD_SIGN_DETECTION_LABELS = path('labels.txt')

detector = vision.Detector(ROAD_SIGN_DETECTION_MODEL_EDGETPU)
labels = read_label_file(ROAD_SIGN_DETECTION_LABELS)


#current_grayscale_value = px.get_grayscale_data()
#camera_feed()

#print(current_grayscale_value)
#filterAndModel(ROAD_SIGN_DETECTION_MODEL_EDGETPU, ROAD_SIGN_DETECTION_LABELS)
for frame in vision.get_frames():
    #objects = detector.get_objects(frame, threshold=0.4)
    #vision.draw_objects(frame, objects, labels)
    height, width = frame.shape[:2]
    balanced = whiteBalanceBullshit(frame)
    #print(width, height)
    edges = process_image(balanced, height, width)
            #angle = calculate_steering_angle(edges, width)
            #control_picarx(angle)
   # cv2.imshow("Processed Frame", edges)
   # cv2.imshow("Frame", balanced)
    lines = cv2.HoughLinesP(edges, rho = 6, theta = np.pi/60, threshold = 160, lines = np.array([]), minLineLength = 40, maxLineGap = 25)
    line_image = draw_lines(edges, lines)
    cv2.imshow("LINES", line_image)
#    if (objects):
#        if (objects[0].id == 2):
#            print("dis bish a stop sign please slip it in")
#            current_grayscale_value = px.get_grayscale_data()
#            #fiugre out greyscale value works correctly
#            if(current_grayscale_value[0]>250 and current_grayscale_value[1]>250 and current_grayscale_value[2]>250):
#                print("stoppiong")
#            print("awake")

from functions import detect_lane_centroids, process_image
from picarx import Picarx
import cv2
import numpy as np
from aiymakerkit import vision
px = Picarx()

while True:
    frame = vision.get_frames()  # Get camera feed
    processed = process_image(frame)  # Process and compute steering
    cv2.imshow("Lane Detection", processed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
px.stop()
#        elif (objects[0].id == 6):
#        
#        elif (objects[0].id == 0):
#           print("dis a mf duck, *smirks*")
