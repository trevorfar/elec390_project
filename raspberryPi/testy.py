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

frame_count = 0  
prev_steering_angle = 0  # Store previous steering angle for smoothing

def calculate_steering_angle(img, lines):
    height, width = img.shape[:2]
    right_lines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1 + 0.0001)  # Avoid division by zero
            if slope > 0.2:  # Ensure we're looking at a reasonable lane line
                right_lines.append((x1, y1, x2, y2))

    if not right_lines:
        print("No right lane detected! Keeping last steering angle.")
        return prev_steering_angle  

    rightmost_line = max(right_lines, key=lambda l: max(l[0], l[2]))
    x1, y1, x2, y2 = rightmost_line
    lane_center_x = (x1 + x2) // 2  
    car_x = width // 2  
    deviation = lane_center_x - car_x
    max_steering = 30
    steering_angle = ((deviation / (width // 2)) * max_steering )

    print(f"Lane Center: {lane_center_x}, Deviation: {deviation}, Steering: {steering_angle:.2f}")
    
    return np.clip(steering_angle, -max_steering, max_steering)

def control_car(steering_angle):
    px.set_dir_servo_angle(int(steering_angle))
    px.forward(20)  # Move forward at a reasonable speed

def detect_lane_edges(img, height, width):
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    roi_points = np.array([
        [0, height],
        [0, 3*height//4],  
        [width//2, 3*height//4],  
        [width//2, height]  
    ], np.int32)

    mask = np.zeros_like(white_mask)
    cv2.fillPoly(mask, [roi_points], 255)

    blurred_white = cv2.GaussianBlur(white_mask, (5, 5), 0)
    white_edges = cv2.Canny(cv2.GaussianBlur(blurred_white, (5, 5), 0), 50, 150)
    
    masked_white = cv2.bitwise_and(white_edges, white_edges, mask=mask)

    return masked_white

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    if lines is None:
        return img
    img = np.copy(img)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    
    return cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

def process_image(img):
    global frame_count, prev_steering_angle
    height, width = img.shape[:2]
    white_edges = detect_lane_edges(img, height, width)
    cv2.imshow("Edges", white_edges)

    lines = cv2.HoughLinesP(
        white_edges,
        rho=6,
        theta=np.pi/60,
        threshold=120,  # Lowered to improve detection in noisy conditions
        minLineLength=30,
        maxLineGap=20
    )

    if lines is not None:
        img = draw_lines(img, lines, color=[0, 255, 0], thickness=3)
        
        # Smooth steering adjustment
        steering_angle = calculate_steering_angle(img, lines)
        smoothed_angle = (0.7 * prev_steering_angle) + (0.3 * steering_angle)  # More stable
        prev_steering_angle = smoothed_angle
        control_car(smoothed_angle)
    else:
        print("No lines detected, maintaining last steering angle.")

    cv2.imshow("Processed", img)
    frame_count += 1
    return img

try:
    for frame in vision.get_frames():
        process_image(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    px.stop()
    cv2.destroyAllWindows()
