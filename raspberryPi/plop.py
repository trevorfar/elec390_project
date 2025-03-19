import os
from picarx import Picarx
import time
import cv2
import numpy as np
from aiymakerkit import vision
import readchar

px = Picarx()

px.set_cam_tilt_angle(-10)
#px.set_cam_pan_angle(pan_angle)

def detect_lane_centroids(img, height, width):
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])

    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # Combine masks
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 0.5, 0)
    
    # --- Triangular ROI ---
    roi_points = np.array([
        [0, height],
        [0, 3*height//4],           # Bottom-left
        #[width // 2, height // 2],  # Middle-top
        [width, 3*height//4],       # Bottom-right
        [width, height]             # Bottom-right
    ], np.int32)

    # Create mask for the ROI
    mask = np.zeros_like(combined)
    cv2.fillPoly(mask, [roi_points], 255)  # Fill the triangular ROI with white

    # Invert mask: Everything outside the ROI is white (shaded area)
    mask_inv = cv2.bitwise_not(mask)

    # Create a full-screen dark overlay
    overlay = img.copy()
    overlay[:] = (0, 100, 0)  # Dark green tint

    # Apply the mask to the overlay (shade only outside ROI)
    shaded_area = cv2.bitwise_and(overlay, overlay, mask=mask_inv)

    # Blend the shaded area with the original image
    alpha = 0.5  # Transparency level
    img[:] = cv2.addWeighted(img, 1, shaded_area, alpha, 0)

    # Draw the ROI boundary in red
    cv2.polylines(img, [roi_points], isClosed=True, color=(0, 0, 255), thickness=2)

    #YELLOW
    blurred_yellow = cv2.GaussianBlur(yellow_mask, (5, 5), 0)
    yellow_edges = cv2.Canny(blurred_yellow, 50, 150)

    #WHITE
    blurred_white = cv2.GaussianBlur(white_mask, (5, 5), 0)
    white_edges = cv2.Canny(blurred_white, 50, 150)

    white_contours, _ = cv2.findContours(white_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, _ = cv2.findContours(yellow_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    white_centroids = []
    yellow_centroids = []
    
    def get_centroids(contours, color):
        centroids = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            
            # Check if centroid is within the ROI
                if cv2.pointPolygonTest(roi_points, (cx, cy), False) >= 0:
                        centroids.append((cx, cy))
                        cv2.circle(img, (cx, cy), 5, color, -1)
        return centroids

    yellow_centroids = get_centroids(yellow_contours, (0, 255, 255))
    white_centroids = get_centroids(white_contours, (255, 255, 255))
    
    return [yellow_centroids, white_centroids] 
    #return db.labels_

def convert_yellow_to_white(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define yellow color range
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Create a mask for yellow
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Replace yellow pixels with white
    img[yellow_mask > 0] = [255, 255, 255]  # Set to white (BGR)

    return img

def draw_best_fit_line(img, centroids, color):
    if len(centroids) < 2: 
        return

    if len(centroids) > 1:  # Ensure enough points for a fit
    # Extract x and y values from centroids
        x_vals = np.array([pt[0] for pt in centroids], dtype=np.float64)
        y_vals = np.array([pt[1] for pt in centroids], dtype=np.float64)

    valid_mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    x_vals, y_vals = x_vals[valid_mask], y_vals[valid_mask]

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
        threshold = 2 * mad
        mask = residuals < threshold

        return x[mask], y[mask]  # Return filtered points

# Remove outliers
    x_vals, y_vals = remove_outliers(x_vals, y_vals)

    if len(x_vals) < 2 or np.app(x_vals == x_vals[0]):  # Ensure we still have enough points
        return  
    try:
        m, b = np.polyfit(x_vals, y_vals, 1)
    except np.linalg.linAlgError:
        return

# Define start and end points for the line
    height = img.shape[0]
    y_start = height  
    y_end = int(3 * height / 4)
    x_start = int((y_start - b) / m)
    x_end = int((y_end - b) / m)



def process_image(img):
    #img = convert_yellow_to_white(img)  # Convert yellow to white first
    height, width = img.shape[:2]  # Get height and width
    #bottom_half = img[h // 2 : h, :]  # Select bottom half explicitly
    #height, width = bottom_half.shape[:2]
    image_center_x = width // 2
    image_center_y = height // 2


    yellow_centroids, white_centroids = detect_lane_centroids(img, height, width)


    # Ensure valid numbers before drawing
    if np.isfinite(x_start) and np.isfinite(x_end):
        cv2.line(img, (x_start, y_start), (x_end, y_end), color, 3) 

    draw_best_fit_line(img, yellow_centroids, (0, 255, 255))  # Yellow line
    draw_best_fit_line(img, white_centroids, (255, 255, 255))  # White line

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        cv2.imwrite("lane_detection_output.jpg", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()  # Ensure the car stops when exiting
    cv2.destroyAllWindows()


