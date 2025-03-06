import cv2
import numpy as np

def process_image(img, height, width):
    # HSV color ranges
    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([255, 30, 255])
    
    # Height to consider
    roi_top = 0.6  
    roi_bottom = 1.0
    

    #HSV -> Yellow and white masks (Road lines)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converts to hsv
    cv2.imwrite('output_images/1_hsv.jpg', hsv)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    cv2.imwrite('output_images/2_yellow_mask.jpg', yellow_mask)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    cv2.imwrite('output_images/3_white_mask.jpg', white_mask)

    # Combine masks with weighting
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0) # combines the masks 
    cv2.imwrite('output_images/4_combined.jpg', combined)
    
    #Masks it to only include half ( we dont need to use the full road yet, just the immediate road )
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[
    (0, int(height * roi_top)), 
    (width, int(height * roi_top)), 
    (width, height), 
    (0, height)
]], dtype=np.int32)

    cv2.fillPoly(mask, roi_vertices, 255)
    roi = cv2.bitwise_and(combined, mask)
    cv2.imwrite('output_images/5_split.jpg', roi)
    
    # Edge detection
    blurred = cv2.GaussianBlur(roi, (5,5), 0)
    cv2.imwrite('output_images/6_blurred.jpg', blurred)
    edges = cv2.Canny(blurred, 50, 150)
    cv2.imwrite('output_images/7_edges.jpg', edges)


# Main stuff
image = cv2.imread('team13_002.jpg')
height, width = image.shape[:2]
process_image(image, height, width)
roi_offset = int(height * 0.4)

print("All done WOOT")
