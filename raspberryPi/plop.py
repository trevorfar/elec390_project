import os
from picarx import Picarx
import time
import cv2
import numpy as np
from aiymakerkit import vision
import readchar
from sklearn.cluster import DBSCAN
from sklearn.linear_model import RANSACRegressor

px = Picarx()
px.set_cam_tilt_angle(-10)

def cluster_centroids(x, y):
    if len(x) < 3:
        return x, y  # Not enough points to cluster

    coords = np.column_stack((x, y))

    # Automatically adjust `eps` based on the data spread
    eps = max(np.std(x), 20)  # Ensure a reasonable neighborhood size
    dbscan = DBSCAN(eps=eps, min_samples=3)
    labels = dbscan.fit_predict(coords)

    unique_labels, counts = np.unique(labels, return_counts=True)
    if len(unique_labels) < 2:
        return x, y  # No clusters found, return original

    largest_cluster_label = unique_labels[np.argmax(counts)]
    mask = labels == largest_cluster_label

    return x[mask], y[mask]

def remove_outliers(x, y):
    if len(x) < 3:
        return x, y

    # Fit an initial rough line
    m, b = np.polyfit(x, y, 1)
    residuals = np.abs(y - (m * x + b))
    
    # Use standard deviation instead of MAD for better accuracy
    std_dev = np.std(residuals)
    threshold = 2.0 * std_dev  # Remove points that deviate too much
    mask = residuals < threshold

    return x[mask], y[mask]

def draw_best_fit_line(img, centroids, color):
    if len(centroids) < 2:
        return

    x_vals = np.array([pt[0] for pt in centroids], dtype=np.float64)
    y_vals = np.array([pt[1] for pt in centroids], dtype=np.float64)

    valid_mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    x_vals, y_vals = x_vals[valid_mask], y_vals[valid_mask]

    # Apply clustering and filtering
    x_vals, y_vals = cluster_centroids(x_vals, y_vals)
    x_vals, y_vals = remove_outliers(x_vals, y_vals)

    if len(x_vals) < 2:
        return

    try:
        # **Use RANSAC instead of np.polyfit for robust line fitting**
        model = RANSACRegressor()
        model.fit(x_vals.reshape(-1, 1), y_vals)
        m, b = model.estimator_.coef_[0], model.estimator_.intercept_
    except:
        return

    height = img.shape[0]
    y_start = height  
    y_end = int(3 * height / 4)
    x_start = int((y_start - b) / m)
    x_end = int((y_end - b) / m)
    cv2.line(img, (x_start, y_start), (x_end, y_end), color, 2)

    # **Actually draw the robust best-fit line**
    cv2.line(img, (x_start, y_start), (x_end, y_end), color, thickness=3)

def process_image(img):
    height, width = img.shape[:2]
    yellow_centroids, white_centroids = detect_lane_centroids(img, height, width)

    draw_best_fit_line(img, yellow_centroids, (0, 255, 255))  # Yellow line
    draw_best_fit_line(img, white_centroids, (255, 255, 255))  # White line

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

