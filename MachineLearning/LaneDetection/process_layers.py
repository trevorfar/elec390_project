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
    
    # Convert to HSV and create masks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # Combine masks
    combined = cv2.addWeighted(yellow_mask, 1.0, white_mask, 1.0, 0)
    
    # Create ROI mask
    mask = np.zeros_like(combined)
    roi_vertices = np.array([[
        (0, int(height * roi_top)), 
        (width, int(height * roi_top)), 
        (width, height), 
        (0, height)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, roi_vertices, 255)
    roi = cv2.bitwise_and(combined, mask)
    
    # Edge detection
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    return edges

# Main function for video processing
def process_video(video_path, output_path=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        
        processed_frame = process_image(frame, height, width)
        
        cv2.imshow("Processed Frame", processed_frame)
        
        if output_path:
            out.write(processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()

video_path = "input_video.mp4"  
output_path = "output_video.mp4" 
process_video(video_path, output_path)
