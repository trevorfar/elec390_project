import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


def process_image(img, height, width):
    # HSV color ranges for lane detection
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    #original 0 0 200
    #original 255 30 255
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

def camera_feed():
    #global process_flag = 1
    process_flag = 1

    # Initialize PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)  # Set resolution
    camera.framerate = 30  # Set frame rate
    raw_capture = PiRGBArray(camera, size=(640, 480))

    # Allow the camera to warm up
    time.sleep(0.1)
    
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # Grab the raw NumPy array representing the image
        image = frame.array

        # Display the raw camera feed
        cv2.imshow("Camera Feed", image)

        # If processing is enabled, process the image and control PiCar-X
        if process_flag:
            height, width = image.shape[:2]
            edges = process_image(image, height, width)
            #angle = calculate_steering_angle(edges, width)
            #control_picarx(angle)
            cv2.imshow("Processed Frame", edges)

        # Clear the stream for the next frame
        raw_capture.truncate(0)

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit
            break
        elif key == ord('p'):  # Toggle processing
            process_flag = not process_flag
            print(f"Processing enabled: {process_flag}")
print("Trevors a cuck")
