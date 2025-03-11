import os

os.environ["DISPLAY"] = ""

from functions import detect_lane_centroids, process_image
from picarx import Picarx
import cv2
import numpy as np
from aiymakerkit import vision
px = Picarx()


for frame in vision.get_frames():
    processed = process_image(frame)  # Process and compute steering
    cv2.imwrite("lane_detection_output.jpg", processed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
px.stop()
