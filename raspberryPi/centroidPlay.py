import os
from picarx import Picarx
import cv2
import numpy as np
from aiymakerkit import vision
from sklearn.cluster import DBSCAN

px = Picarx()


def brighten_yellow_and_white(image, brightness_factor=1.5):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the color ranges for yellow and white in HSV space
    lower_yellow = np.array([20, 100, 100])  # Lower bound for yellow
    upper_yellow = np.array([40, 255, 255])  # Upper bound for yellow
    lower_white = np.array([0, 0, 200])  # Lower bound for white
    upper_white = np.array([180, 50, 255])  # Upper bound for white

    # Create masks for yellow and white colors
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(hsv_image, lower_white, upper_white)

    # Combine the masks (yellow + white)
    mask = cv2.bitwise_or(mask_yellow, mask_white)
    
    # Convert the image back to BGR for processing
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    # Brighten the selected pixels (yellow and white)
    bgr_image = np.where(mask[:, :, None] == 255, np.clip(bgr_image * brightness_factor, 0, 255), bgr_image)

    # Convert the result back to BGR
    result = np.uint8(bgr_image)

    return result

def detect_lane_centroids_yellow(img, height, width):
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    #white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # Combine masks
    #combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)

    # --- Triangular ROI ---
    roi_points = np.array([
        [0, height],
        [0, 3*height//4],           # Bottom-left
        [width // 2, height // 2],  # Middle-top
        [width, 3*height//4],       # Bottom-right
        [width, height]             # Bottom-right
    ], np.int32)

    # Create mask for the ROI
    mask = np.zeros_like(yellow_mask)
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

    # Apply preprocessing
    blurred = cv2.GaussianBlur(yellow_mask, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    cv2.imshow("EDGES", edges)
    # Find contours
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centroid_points = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Check if centroid is within the ROI
            if cv2.pointPolygonTest(roi_points, (cx, cy), False) >= 0:
                centroid_points.append((cx, cy))
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)  # Draw valid centroids

    
    return centroid_points

def detect_lane_centroids_white(img, height, width):
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])

    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # Combine masks
    #combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)

    # --- Triangular ROI ---
    roi_points = np.array([
        [0, height],
        [0, 3*height//4],           # Bottom-left
        [width // 2, height // 2],  # Middle-top
        [width, 3*height//4],       # Bottom-right
        [width, height]             # Bottom-right
    ], np.int32)

    # Create mask for the ROI
    mask = np.zeros_like(white_mask)
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

    # Apply preprocessing
    blurred = cv2.GaussianBlur(white_mask, (5, 5), 0)
    edges = cv2.Canny(white_mask, 50, 150)
    cv2.imshow("EDGES", edges)
    # Find contours
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centroid_points = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Check if centroid is within the ROI
            if cv2.pointPolygonTest(roi_points, (cx, cy), False) >= 0:
                centroid_points.append((cx, cy))
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)  # Draw valid centroids

    
    return centroid_points
    #return db.labels_

def process_image(img):
    height, width = img.shape[:2]
    image_center_x = width // 2
    image = brighten_yellow_and_white(img, brightness_factor=10)
    centroid_points_yellow = detect_lane_centroids_yellow(image, height, width)
    centroid_points_white = detect_lane_centroids_white(image, height, width)

    return image

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        cv2.imwrite("lane_detection_output.jpg", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()  # Ensure the car stops when exiting
    cv2.destroyAllWindows()

