import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

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
def process_picarx_video(output_path=None):
    # Initialize PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30  
    raw_capture = PiRGBArray(camera, size=(640, 480))
    
    # Allow the camera to warm up
    time.sleep(0.1)
    
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        out = cv2.VideoWriter(output_path, fourcc, 30, (640, 480), isColor=False)
    
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        
        processed_frame = process_image(image, 480, 640)
        
        # Display the processed frame
        cv2.imshow("Processed Frame", processed_frame)
        
        # Save the processed frame if output path is provided
        if output_path:
            out.write(processed_frame)
        
        # Clear the stream for the next frame
        raw_capture.truncate(0)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    camera.close()
    if output_path:
        out.release()
    cv2.destroyAllWindows()

# Run the PiCar-X video processing
output_path = "output_video.mp4"  # Optional: Save the processed video
process_picarx_video(output_path)
