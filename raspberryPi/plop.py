import os
from picarx import Picarx
import time
import cv2
import numpy as np
from aiymakerkit import vision
import readchar
from sklearn.linear_model import RANSACRegressor
import matplotlib.pyplot as plt
px = Picarx()
px.set_cam_tilt_angle(-10)

def calculate_steering_angle(img, lines):
    height, width = img.shape[:2]
    right_lines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1 + 0.0001)  # Avoid division by zero
            if slope > 0.3:  # Right lane detection (adjust slope threshold if needed)
                right_lines.append((x1, y1, x2, y2))

    if not right_lines:
        print("No right lane detected!")
        return 0  # Keep the car going straight if no right lane is detected

    rightmost_line = max(right_lines, key=lambda l: max(l[0], l[2]))
    x1, y1, x2, y2 = rightmost_line
    lane_center_x = (x1 + x2) // 2  
    car_x = width // 2  
    deviation = lane_center_x - car_x
    max_steering = 30
    steering_angle = (deviation / (width // 2)) * max_steering
    return np.clip(steering_angle, -max_steering, max_steering)


def control_car(steering_angle):    
    servo_angle = int(steering_angle)
    px.set_dir_servo_angle(servo_angle)
    px.forward(10)  # Adjust speed based on your testing

    print(f"Steering: {servo_angle}°")


def detect_lane_edges(img, height, width):
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    cv2.imshow("white_mask", white_mask)

    roi_points = np.array([
        [0, height],
        [0, 3*height//4],  
        [width, 3*height//4],  
        [width, height]  
    ], np.int32)

    mask = np.zeros_like(white_mask)
    cv2.fillPoly(mask, [roi_points], 255)

    blurred_white = cv2.GaussianBlur(white_mask, (5, 5), 0)
    white_edges = cv2.Canny(cv2.GaussianBlur(blurred_white, (5, 5), 0), 50, 150)
    
    mask_inv = cv2.bitwise_not(mask)
    overlay = img.copy()
    overlay[:] = (0, 100, 0)
    shaded_area = cv2.bitwise_and(overlay, overlay, mask=mask_inv)
    alpha = 0.5
    img[:] = cv2.addWeighted(img, 1, shaded_area, alpha, 0)
    
    masked_white = cv2.bitwise_and(white_edges, white_edges, mask=mask)

    cv2.polylines(img, [roi_points], isClosed=True, color=(0, 0, 255), thickness=2)
    
   

    return masked_white, mask

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
    y_start, y_end = model.predict(np.array([[x_start], [x_end]])).flatten()
    cv2.line(img, (int(x_start), int(y_start)), (int(x_end), int(y_end)), color, 2)

def draw_lines(img, lines, color=[255, 0 ,0], thickness = 3):
    if lines is None:
        return
    img = np.copy(img)
    line_img = np.zeros((
        img.shape[0],
        img.shape[1],
        3
    ),
    dtype=np.uint8
    )
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    return img

def process_image(img):
    height, width = img.shape[:2]
    white_edges, roi_mask = detect_lane_edges(img, height, width)
    cv2.imshow("white", white_edges)

    lines = cv2.HoughLinesP(
     white_edges,
     rho=6,
     theta=np.pi/60,
     threshold=160,
     lines=np.array([]),
     minLineLength=40,
     maxLineGap=25
    )
    if lines is not None:
        img = draw_lines(img, lines, color=[0, 255, 0], thickness=3)
        steering_angle = calculate_steering_angle(img, lines)
        control_car(steering_angle)
    
    cv2.imshow("hough", img)
    return img

try:
    for frame in vision.get_frames():
        processed = process_image(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()
    cv2.destroyAllWindows()