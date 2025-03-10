import cv2
import numpy as np

def process_image(img, height, width):
    # HSV color ranges
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])
    
    # Region of Interest (ROI) bounds
    roi_top = 0.6  
    roi_bottom = 1.0  

    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    
    # Combine masks
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)
    
    # Mask for region of interest
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[
        (0, int(height * roi_top)), 
        (width, int(height * roi_top)), 
        (width, height), 
        (0, height)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, roi_vertices, 255)
    
    # Apply ROI mask
    roi = cv2.bitwise_and(combined, mask)
    
    # Edge detection
    blurred = cv2.GaussianBlur(roi, (5,5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Compute centroids
    centroid_points = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroid_points.append((cx, cy))
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)  # Draw centroids

    # Save output images for debugging
    cv2.imwrite('output_images/1_hsv.jpg', hsv)
    cv2.imwrite('output_images/2_yellow_mask.jpg', yellow_mask)
    cv2.imwrite('output_images/3_white_mask.jpg', white_mask)
    cv2.imwrite('output_images/4_combined.jpg', combined)
    cv2.imwrite('output_images/5_roi.jpg', roi)
    cv2.imwrite('output_images/6_blurred.jpg', blurred)
    cv2.imwrite('output_images/7_edges.jpg', edges)
    cv2.imwrite('output_images/8_centroids.jpg', img)

    return centroid_points  # Return centroids for further processing

# Main execution
image = cv2.imread('team13_002.jpg')
height, width = image.shape[:2]
centroids = process_image(image, height, width)

print("Centroids detected:", centroids)
print("All done WOOT")

