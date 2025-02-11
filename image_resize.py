import cv2
import os
import re

input_folder = "./original_photos"
output_folder = "./original_photos/new_photos"

os.makedirs(output_folder, exist_ok=True)

existing_numbers = []
pattern = re.compile(r"team13_(\d{3})")

for existing_file in os.listdir(output_folder):
    match = pattern.search(existing_file)
    if match:
        existing_numbers.append(int(match.group(1)))

next_number = max(existing_numbers, default=-1) + 1  # Start from 000 if no files exist

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        resized_img = cv2.resize(img, (320, 320))
        
        new_filename = f"team13_{next_number:03d}{os.path.splitext(filename)[1]}"
        next_number += 1
        
        new_img_path = os.path.join(output_folder, new_filename)
        cv2.imwrite(new_img_path, resized_img)
        
        os.remove(img_path)

print("Resizing, renaming, and removing original files complete!")
