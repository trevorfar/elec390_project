from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import os
import tflite_runtime.interpreter as tflite
from pycoral.adapters import common, detect
from pycoral.utils.dataset import read_label_file

# Paths
images_path = "/content/split-dataset/train/images"
filenames = os.listdir(images_path)
random_index = random.randint(0, len(filenames) - 1)
INPUT_IMAGE = os.path.join(images_path, filenames[random_index])

TFLITE_FILENAME = 'efficientdet-lite.tflite'  # Generalized model name
LABELS_FILENAME = 'labels.txt'  # Generalized label file

# Load labels
labels = read_label_file(LABELS_FILENAME)

# Load model
interpreter = tflite.Interpreter(TFLITE_FILENAME)
interpreter.allocate_tensors()

# Load image
image = Image.open(INPUT_IMAGE)
_, scale = common.set_resized_input(
    interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))

# Run inference
interpreter.invoke()
objs = detect.get_objects(interpreter, score_threshold=0.4, image_scale=scale)

# Generate colors for labels dynamically
label_colors = {label_id: tuple(np.random.randint(0, 255, size=3).tolist()) for label_id in labels.keys()}

def draw_objects(draw, objs, scale_factor, labels):
    """Draw bounding boxes and labels for detected objects."""
    for obj in objs:
        bbox = obj.bbox
        color = label_colors.get(obj.id, (255, 255, 255))  # Default to white if missing
        draw.rectangle([(bbox.xmin * scale_factor, bbox.ymin * scale_factor),
                        (bbox.xmax * scale_factor, bbox.ymax * scale_factor)],
                       outline=color, width=3)
        font = ImageFont.truetype("LiberationSans-Regular.ttf", size=15)
        label_text = f"{labels.get(obj.id, 'Unknown')} ({obj.score:.2f})"
        draw.text((bbox.xmin * scale_factor + 4, bbox.ymin * scale_factor + 4),
                  label_text, fill=color, font=font)

# Resize image for visualization
display_width = 500
scale_factor = display_width / image.width
height_ratio = image.height / image.width
image = image.resize((display_width, int(display_width * height_ratio)))

# Draw objects
draw_objects(ImageDraw.Draw(image), objs, scale_factor, labels)

# Save output image
image.save("detection-result.jpg")

