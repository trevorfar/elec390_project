import cv2
import numpy as np

def detect_lane_markings(img, height, width):
    # HSV color ranges
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])
    
    # ROI parameters
    roi_top = 0.5  # Ignore top 40%
    roi_bottom = 0.5  # Focus on lower 60%
    
    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    
    # Combine masks with weighting
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 0.5, 0)
    
    # ROI Masking instead of Cropping
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[(0, height), (width, height), (width, int(height * roi_bottom)), (0, int(height * roi_bottom))]], dtype=np.int32)
    cv2.fillPoly(mask, roi_vertices, 255)
    roi = cv2.bitwise_and(combined, mask)
    
    # Edge detection
    blurred = cv2.GaussianBlur(roi, (5,5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Hough line detection with a fallback
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 20, minLineLength=30, maxLineGap=10)
    if lines is None:
        lines = []
    
    return lines, roi, edges

def classify_lines(lines, img_width):
    left_lines = []
    right_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        dx = x2 - x1
        dy = y2 - y1
        
        # Ensure the line is not too horizontal
        if abs(dy) < abs(dx) * 0.5:  # Filters out near-horizontal lines
            continue
        
        midpoint_x = (x1 + x2) / 2
        slope = dy / dx if dx != 0 else float('inf')
        
        if midpoint_x < img_width * 0.5 and slope < 0:  # Left lane (negative slope)
            left_lines.append(line[0])
        elif midpoint_x >= img_width * 0.5 and slope > 0:  # Right lane (positive slope)
            right_lines.append(line[0])
    
    return left_lines, right_lines

def draw_adjusted_lines(img, lines, color, side, height, roi_offset):
    for line in lines:
        x1, y1, x2, y2 = line
        y1 += roi_offset
        y2 += roi_offset
        
        # Extend lines to the bottom of the image
        if side == 'left':
            new_y1 = height
            new_x1 = int(x1 + (new_y1 - y1) * (x2 - x1) / (y2 - y1))
            cv2.line(img, (new_x1, new_y1), (x1, y1), color, 3)
        else:
            new_y2 = height
            new_x2 = int(x2 + (new_y2 - y2) * (x1 - x2) / (y1 - y2))
            cv2.line(img, (new_x2, new_y2), (x2, y2), color, 3)

def calculate_position(left, right, img_width):
    if not left or not right:
        return "Lane keeping mode"
    
    left_x = np.mean([x2 for _, _, x2, _ in left]) if left else 0
    right_x = np.mean([x2 for _, _, x2, _ in right]) if right else img_width
    lane_center = (left_x + right_x) / 2
    offset = (lane_center - img_width / 2) / (img_width / 2)
    
    if abs(offset) < 0.1:
        return "Centered"
    return "Drifting left" if offset < 0 else "Drifting right"

# Main Processing
image = cv2.imread('team13_009.jpg')
height, width = image.shape[:2]
lines, roi, edges = detect_lane_markings(image, height, width)
left_lines, right_lines = classify_lines(lines, width)
output = image.copy()
roi_offset = int(height * 0.4)

draw_adjusted_lines(output, left_lines, (0, 0, 255), 'left', height, roi_offset)
draw_adjusted_lines(output, right_lines, (0, 255, 0), 'right', height, roi_offset)

position = calculate_position(left_lines, right_lines, width)
cv2.putText(output, position, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imwrite('lane_output.jpg', output)
print("Processing complete - output saved as lane_output.jpg")
