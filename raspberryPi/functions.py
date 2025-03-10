import numpy as np
import cv2
from picarx import Picarx


def detect_lane_centroids(img, height, width):
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])
    
    roi_top = 0.6  
    roi_bottom = 1.0  

    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    
    # Combine masks
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)
    
    # Mask for region of interest
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[
        (0, int(height * roi_top)), 
        (width, int(height * roi_top)), 
        (width, height), 
        (0, height)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, roi_vertices, 255)
    roi = cv2.bitwise_and(combined, mask)
    blurred = cv2.GaussianBlur(roi, (5,5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    centroid_points = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroid_points.append((cx, cy))
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 
    return centroid_points




def process_image(img):
    height, width = img.shape[:2]
    image_center_x = width // 2

    centroid_points = detect_lane_centroids(img, height, width)
    if len(centroid_points) > 0:
        lowest_centroid = max(centroid_points, key=lambda p: p[1])
        target_x, _ = lowest_centroid
        error = target_x - image_center_x
        Kp = 0.1 
        steering_angle = np.clip(Kp * error, -30, 30)
        px.set_dir_servo_angle(steering_angle)
        print(f"Steering angle: {steering_angle}")
    return img
