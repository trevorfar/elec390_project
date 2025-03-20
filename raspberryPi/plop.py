import os
from picarx import Picarx
import time
import cv2
import numpy as np
from aiymakerkit import vision
import readchar
from sklearn.linear_model import RANSACRegressor

px = Picarx()
px.set_cam_tilt_angle(-10)

def detect_lane_edges(img, height, width):
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 0.5, 0)

    roi_points = np.array([
        [0, height],
        [0, 3*height//4],  
        [width, 3*height//4],  
        [width, height]  
    ], np.int32)

    mask = np.zeros_like(combined)
    cv2.fillPoly(mask, [roi_points], 255)
    
    blurred_yellow = cv2.GaussianBlur(yellow_mask, (5, 5), 0)
    yellow_edges = cv2.Canny(cv2.GaussianBlur(blurred_yellow, (5, 5), 0), 50, 150)
    
    blurred_white = cv2.GaussianBlur(white_mask, (5, 5), 0)
    white_edges = cv2.Canny(cv2.GaussianBlur(blurred_white, (5, 5), 0), 50, 150)
    
    mask_inv = cv2.bitwise_not(mask)
    overlay = img.copy()
    overlay[:] = (0, 100, 0)
    shaded_area = cv2.bitwise_and(overlay, overlay, mask=mask_inv)
    alpha = 0.5
    img[:] = cv2.addWeighted(img, 1, shaded_area, alpha, 0)
    
    masked_yellow = cv2.bitwise_and(yellow_edges, yellow_edges, mask=mask)
    masked_white = cv2.bitwise_and(white_edges, white_edges, mask=mask)

    cv2.polylines(img, [roi_points], isClosed=True, color=(0, 0, 255), thickness=2)
    
   

    return masked_yellow, masked_white, mask

def extract_edge_points(edges):
    points = np.column_stack(np.where(edges > 0))
    return points[:, 1], points[:, 0]  # Return x, y coordinates

def draw_best_fit_line(img, x_vals, y_vals, color):
    if len(x_vals) < 2:
        return

    x_vals, y_vals = np.array(x_vals), np.array(y_vals)

    # Use RANSAC to remove outliers
    model = RANSACRegressor()
    model.fit(x_vals.reshape(-1, 1), y_vals)
    
    x_start, x_end = np.min(x_vals), np.max(x_vals)
    y_start, y_end = model.predict([[x_start], [x_end]])

    cv2.line(img, (int(x_start), int(y_start)), (int(x_end), int(y_end)), color, 2)

def process_image(img):
    height, width = img.shape[:2]
    yellow_edges, white_edges, roi_mask = detect_lane_edges(img, height, width)
    
    yellow_edges_colored = cv2.cvtColor(yellow_edges, cv2.COLOR_GRAY2BGR)
    white_edges_colored = cv2.cvtColor(white_edges, cv2.COLOR_GRAY2BGR)
    
    yellow_edges_colored[:] = (0, 0, 0)
    white_edges_colored[:] = (0, 0, 0)
    
    img_with_edges = cv2.addWeighted(img, 1, yellow_edges_colored, 0.7, 0)
    img_with_edges = cv2.addWeighted(img_with_edges, 1, white_edges_colored, 0.7, 0)
    
    yellow_x, yellow_y = extract_edge_points(yellow_edges)
    white_x, white_y = extract_edge_points(white_edges)

    draw_best_fit_line(img, yellow_x, yellow_y, (0, 255, 255))
    draw_best_fit_line(img, white_x, white_y, (255, 255, 255))

    return img

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        #cv2.imwrite("lane_detection_output.jpg", processed)
        cv2.imshow("lane detection", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()
    cv2.destroyAllWindows()