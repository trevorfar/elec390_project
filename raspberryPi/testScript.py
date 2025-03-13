import cv2
import numpy as np
import matplotlib.pyplot as plt

def brighten_yellow_and_white(image, brightness_factor=1.5):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow, upper_yellow = np.array([20, 100, 100]), np.array([40, 255, 255])
    lower_white, upper_white = np.array([0, 0, 200]), np.array([180, 50, 255])
    
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(hsv_image, lower_white, upper_white)
    mask = cv2.bitwise_or(mask_yellow, mask_white)
    
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    bgr_image = np.where(mask[:, :, None] == 255, np.clip(bgr_image * brightness_factor, 0, 255), bgr_image)
    return np.uint8(bgr_image)

def detect_lane_centroids(img, lower_color, upper_color, color=(255, 0, 0)):
    height, width = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    roi_points = np.array([
        [0, height], [0, 3*height//4], [width // 2, height // 2],
        [width, 3*height//4], [width, height]
    ], np.int32)
    
    mask_roi = np.zeros_like(mask)
    cv2.fillPoly(mask_roi, [roi_points], 255)
    mask = cv2.bitwise_and(mask, mask_roi)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centroid_points = []
    
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            if cv2.pointPolygonTest(roi_points, (cx, cy), False) >= 0:
                centroid_points.append((cx, cy))
                cv2.circle(img, (cx, cy), 5, color, -1)
    
    return centroid_points

def draw_best_fit_line(img, centroids, color):
    if len(centroids) > 1:
        centroids = np.array(centroids)
        x, y = centroids[:, 0], centroids[:, 1]
        
        poly_coeff = np.polyfit(x, y, 1)  # Linear fit
        poly_func = np.poly1d(poly_coeff)
        
        x_vals = np.linspace(min(x), max(x), 100).astype(int)
        y_vals = poly_func(x_vals).astype(int)
        
        for i in range(len(x_vals) - 1):
            cv2.line(img, (x_vals[i], y_vals[i]), (x_vals[i + 1], y_vals[i + 1]), color, 2)

def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return
    
    img = brighten_yellow_and_white(img, brightness_factor=10)
    yellow_centroids = detect_lane_centroids(img, np.array([15, 100, 100]), np.array([30, 255, 255]), color=(255, 0, 0))  # Yellow
    white_centroids = detect_lane_centroids(img, np.array([0, 0, 200]), np.array([255, 30, 255]), color=(0, 255, 0))  # White
    
    draw_best_fit_line(img, yellow_centroids, (255, 0, 0))  # Draw yellow lane line
    draw_best_fit_line(img, white_centroids, (0, 255, 0))  # Draw white lane line
    
    cv2.imwrite(output_path, img)
    cv2.imshow("Processed Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
process_image("input.jpg", "output.jpg")
import cv2
import numpy as np
import matplotlib.pyplot as plt

def brighten_yellow_and_white(image, brightness_factor=1.5):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow, upper_yellow = np.array([20, 100, 100]), np.array([40, 255, 255])
    lower_white, upper_white = np.array([0, 0, 200]), np.array([180, 50, 255])
    
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(hsv_image, lower_white, upper_white)
    mask = cv2.bitwise_or(mask_yellow, mask_white)
    
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    bgr_image = np.where(mask[:, :, None] == 255, np.clip(bgr_image * brightness_factor, 0, 255), bgr_image)
    return np.uint8(bgr_image)

def detect_lane_centroids(img, lower_color, upper_color, color=(255, 0, 0)):
    height, width = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    roi_points = np.array([
        [0, height], [0, 3*height//4], [width // 2, height // 2],
        [width, 3*height//4], [width, height]
    ], np.int32)
    
    mask_roi = np.zeros_like(mask)
    cv2.fillPoly(mask_roi, [roi_points], 255)
    mask = cv2.bitwise_and(mask, mask_roi)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centroid_points = []
    
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            if cv2.pointPolygonTest(roi_points, (cx, cy), False) >= 0:
                centroid_points.append((cx, cy))
                cv2.circle(img, (cx, cy), 5, color, -1)
    
    return centroid_points

def draw_best_fit_line(img, centroids, color):
    if len(centroids) > 1:
        centroids = np.array(centroids)
        x, y = centroids[:, 0], centroids[:, 1]
        
        poly_coeff = np.polyfit(x, y, 1)  # Linear fit
        poly_func = np.poly1d(poly_coeff)
        
        x_vals = np.linspace(min(x), max(x), 100).astype(int)
        y_vals = poly_func(x_vals).astype(int)
        
        for i in range(len(x_vals) - 1):
            cv2.line(img, (x_vals[i], y_vals[i]), (x_vals[i + 1], y_vals[i + 1]), color, 2)

def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return
    
    img = brighten_yellow_and_white(img, brightness_factor=10)
    yellow_centroids = detect_lane_centroids(img, np.array([15, 100, 100]), np.array([30, 255, 255]), color=(255, 0, 0))  # Yellow
    white_centroids = detect_lane_centroids(img, np.array([0, 0, 200]), np.array([255, 30, 255]), color=(0, 255, 0))  # White
    
    draw_best_fit_line(img, yellow_centroids, (255, 0, 0))  # Draw yellow lane line
    draw_best_fit_line(img, white_centroids, (0, 255, 0))  # Draw white lane line
    
    cv2.imwrite(output_path, img)
    cv2.imshow("Processed Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
process_image("team13_002.jpg", "output.jpg")

