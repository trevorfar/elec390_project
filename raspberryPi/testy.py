import os
from picarx import Picarx
import cv2
import numpy as np
from aiymakerkit import vision

px = Picarx()

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
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)

    # --- Triangular ROI ---
    roi_points = np.array([
        [0, height],
	[0, 3*height//4], 	         # Bottom-left
        [width // 2, height // 2],  # Middle-top
	[width, 3*height//4],	
        [width, height]      # Bottom-right
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

    # Apply preprocessing
    blurred = cv2.GaussianBlur(combined, (5,5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

def process_image(img):
    height, width = img.shape[:2]
    image_center_x = width // 2

    centroid_points = detect_lane_centroids(img, height, width)
    if len(centroid_points) > 0:
        lowest_centroid = max(centroid_points, key=lambda p: p[1])
        target_x, _ = lowest_centroid
        error = target_x - image_center_x

        # Steering control (P-controller)
        Kp_steering = 0.1 
        steering_angle = np.clip(Kp_steering * error, -30, 30)
        px.set_dir_servo_angle(steering_angle)

        # Speed control: Slow down if turning sharply
        Kp_speed = 1.5  # Adjust speed based on centering error
        base_speed = 30  # Base speed when centered
        speed_adjustment = max(10, base_speed - abs(Kp_speed * error))  # Min speed of 10
        px.forward(speed_adjustment)

        print(f"Steering: {steering_angle:.2f}, Speed: {speed_adjustment:.2f}")
    else:
        # Stop if no lane detected
        px.stop()

    return img

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        cv2.imwrite("lane_detection_output.jpg", processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()  # Ensure the car stops when exiting
    cv2.destroyAllWindows()

