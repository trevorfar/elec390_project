import cv2
import os
import re
from pillow_heif import register_heif_opener
from PIL import Image

# Register HEIF support for PIL
register_heif_opener()

input_folder = "./original_photos"
output_folder = "./original_photos/new_photos"

os.makedirs(output_folder, exist_ok=True)

existing_numbers = []
pattern = re.compile(r"team13_(\d{3})\.jpg")  # Ensures it checks for .jpg files

# Find existing numbering in the output folder
for existing_file in os.listdir(output_folder):
    match = pattern.search(existing_file)
    if match:
        existing_numbers.append(int(match.group(1)))

# Determine the next available number
next_number = max(existing_numbers, default=-1) + 1  

# Process all files in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    
    # Convert HEIC to JPG
    if filename.lower().endswith(".heic"):
        try:
            img = Image.open(file_path)
            img = img.convert("RGB")  # Convert HEIC to RGB mode
        except Exception as e:
            print(f"Skipping {filename}: Unable to process HEIC ({e})")
            continue
    else:
        img = cv2.imread(file_path)
        if img is None:
            continue  # Skip non-image files or unreadable images

    # Resize image to 320x320
    if isinstance(img, Image.Image):  # If using PIL for HEIC
        img = img.resize((320, 320))
    else:
        img = cv2.resize(img, (320, 320))

    # Create new filename as .jpg
    new_filename = f"team13_{next_number:03d}.jpg"
    next_number += 1
    new_img_path = os.path.join(output_folder, new_filename)

    # Save as .jpg
    if isinstance(img, Image.Image):
        img.save(new_img_path, "JPEG", quality=95)
    else:
        cv2.imwrite(new_img_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    # Remove original file
    os.remove(file_path)

print("Processing complete: all images resized, converted to .jpg, and originals removed.")

