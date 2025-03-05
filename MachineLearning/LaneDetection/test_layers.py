import cv2
import numpy as np

# Load image in BGR format
image = cv2.imread('team13_002.jpg')

# Parameters for white and yellow line detection
white_lower = np.array([0, 0, 200])    # Lower HSV threshold for white
white_upper = np.array([255, 30, 255]) # Upper HSV threshold for white

yellow_lower = np.array([20, 100, 100])  # Lower HSV threshold for yellow
yellow_upper = np.array([30, 255, 255]) # Upper HSV threshold for yellow

# Gaussian blur kernel size
gaussian_kernel = (7, 7)

# Canny edge detection thresholds
canny_thresholds = (50, 150)

# Hough Transform parameters (adjusted for dotted lines)
hough_params = (1, np.pi/180, 30, 20, 50)  # rho, theta, threshold, minLineLength, maxLineGap

# Region of Interest (crop top half of the image)
roi_height_ratio = 0.6

# Processing pipeline
def process_image(img):
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create binary masks for white and yellow lines
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    
    # Use morphological operations to connect dotted yellow lines
    kernel = np.ones((9, 9), np.uint8)  # Kernel size for dilation
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=2)  # Increase iterations to connect larger gaps
    
    # Combine masks
    combined_mask = cv2.bitwise_or(white_mask, yellow_mask)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(combined_mask, gaussian_kernel, 0)
    
    # Canny edge detection
    edges = cv2.Canny(blurred, *canny_thresholds)
    
    # Crop top half (keep bottom half)
    height = img.shape[0]
    cropped = edges[int(height * roi_height_ratio):, :]
    
    # Probabilistic Hough Transform
    lines = cv2.HoughLinesP(cropped, *hough_params)
    
    return {
        'original': img,
        'hsv': hsv,
        'white_mask': white_mask,
        'yellow_mask': yellow_mask,
        'combined_mask': combined_mask,
        'edges': edges,
        'cropped': cropped,
        'lines': lines
    }

# Process the image
results = process_image(image)

# Function to calculate line positions
def calculate_line_positions(lines, height, width):
    left_lines = []
    right_lines = []
    center_lines = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Avoid division by zero
            
            # Classify lines based on slope and position
            if slope < -0.5:  # Left lane line (negative slope)
                left_lines.append((x1, y1, x2, y2))
            elif slope > 0.5:  # Right lane line (positive slope)
                right_lines.append((x1, y1, x2, y2))
            else:  # Center line (near horizontal)
                center_lines.append((x1, y1, x2, y2))
    
    return left_lines, right_lines, center_lines

# Calculate line positions
height, width = image.shape[:2]
left_lines, right_lines, center_lines = calculate_line_positions(results['lines'], height, width)

# Draw detected lines on the original image
output = image.copy()

def draw_lines(image, lines, color, thickness=3):
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(image, (x1, y1 + int(height * roi_height_ratio)), 
                 (x2, y2 + int(height * roi_height_ratio)), color, thickness)

# Draw left lines (white)
draw_lines(output, left_lines, (255, 0, 0))  # Blue for left lines

# Draw right lines (white)
draw_lines(output, right_lines, (0, 255, 0))  # Green for right lines

# Draw center lines (yellow)
draw_lines(output, center_lines, (0, 0, 255))  # Red for center lines

# Calculate car position relative to center line
def calculate_car_position(center_lines, width):
    if len(center_lines) > 0:
        # Average x-position of center lines
        avg_x = np.mean([(x1 + x2) / 2 for x1, _, x2, _ in center_lines])
        # Car position relative to center line
        if avg_x < width / 2:
            return "Left of center"
        else:
            return "Right of center"
    return "No center line detected"

car_position = calculate_car_position(center_lines, width)
cv2.putText(output, f"Position: {car_position}", (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Save the final output image
cv2.imwrite('lane_detection_output.jpg', output)
print("Output saved as lane_detection_output.jpg")

# Save intermediate steps (optional)
cv2.imwrite('white_mask.jpg', results['white_mask'])
cv2.imwrite('yellow_mask.jpg', results['yellow_mask'])
cv2.imwrite('edges.jpg', results['edges'])
cv2.imwrite('cropped_edges.jpg', results['cropped'])
print("Intermediate steps saved as white_mask.jpg, yellow_mask.jpg, edges.jpg, cropped_edges.jpg")
