from functions.py import detect_lane_centroids, process_image
from picarx import Picarx
import cv2
import numpy as np

px = Picarx()

while True:
    frame = px.get_image()  # Get camera feed
    processed = process_image(frame)  # Process and compute steering
    cv2.imshow("Lane Detection", processed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
px.stop()
