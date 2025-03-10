import numpy as np
import cv2
import matplotlib.pyplot as plt
from aiymakerkit import vision
from aiymakerkit import utils
from pycoral.utils.dataset import read_label_file
from picarx import Picarx
from utils import camera_feed


position = np.array([0, 1])
velocity = np.array([2, 3])

new_position = position +velocity
print("NEW POSITION:", new_position)

camera_feed()