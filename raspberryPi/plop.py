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

    yellow_edges = cv2.Canny(cv2.GaussianBlur(yellow_mask, (5, 5), 0), 50, 150)
    white_edges = cv2.Canny(cv2.GaussianBlur(white_mask, (5, 5), 0), 50, 150)

    return yellow_edges, white_edges, mask

def extract_edge_points(edges):
    points = np.column_stack(np.where(edges > 0))
    return points[:, 1], points[:, 0]  # Return x, y coordinates

def draw_best_fit_line(img, x_vals, y_vals, color):
    if len(x_vals) < 2:
        return

<<<<<<< HEAD
    if len(centroids) > 1:  # Ensure enough points for a fit
    # Extract x and y values from centroids
        x_vals = np.array([pt[0] for pt in centroids], dtype=np.float64)
        y_vals = np.array([pt[1] for pt in centroids], dtype=np.float64)

    valid_mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    x_vals, y_vals = cluster_centroids(x_vals, y_vals) 

    if len(x_vals) < 2 or np.all(x_vals == x_vals[0]): 
        return

    # Outlier filtering using Median Absolute Deviation (MAD)
    def remove_outliers(x, y):
        if len(x) < 3:  # Not enough points to filter
            return x, y

    # Fit initial line to get residuals
        m, b = np.polyfit(x, y, 1)
        residuals = np.abs(y - (m * x + b))  # Distance from line

    # Compute MAD (Median Absolute Deviation)
        mad = np.median(residuals)

    # Filter: Keep points within a reasonable range (2 * MAD)
        threshold = 1.5 * mad
        mask = residuals < threshold

        return x[mask], y[mask]  # Return filtered points

# Remove outliers
    x_vals, y_vals = remove_outliers(x_vals, y_vals)

    if (len(x_vals) < 2):  # Ensure we still have enough points
        return  
    try:
        m, b = np.polyfit(x_vals, y_vals, 1)
    except np.linalg.LinAlgError:
        return

# Define start and end points for the line
    height = img.shape[0]
    y_start = height  
    y_end = int(3 * height / 4)
    x_start = int((y_start - b) / m)
    x_end = int((y_end - b) / m)
    cv2.line(img, (x_start, y_start), (x_end, y_end), color, 2)
=======
    x_vals, y_vals = np.array(x_vals), np.array(y_vals)
>>>>>>> fbe279fcf6ce0fc7502c5e74d2be78635a2f0a7b

    # Use RANSAC to remove outliers
    model = RANSACRegressor()
    model.fit(x_vals.reshape(-1, 1), y_vals)
    
    x_start, x_end = np.min(x_vals), np.max(x_vals)
    y_start, y_end = model.predict([[x_start], [x_end]])

    cv2.line(img, (int(x_start), int(y_start)), (int(x_end), int(y_end)), color, 2)

def process_image(img):
    height, width = img.shape[:2]
    yellow_edges, white_edges, roi_mask = detect_lane_edges(img, height, width)

    yellow_x, yellow_y = extract_edge_points(yellow_edges)
    white_x, white_y = extract_edge_points(white_edges)

    draw_best_fit_line(img, yellow_x, yellow_y, (0, 255, 255))
    draw_best_fit_line(img, white_x, white_y, (255, 255, 255))

    return img

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        cv2.imwrite("lane_detection_output.jpg", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()
    cv2.destroyAllWindows()

