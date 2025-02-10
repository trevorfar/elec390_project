import cv2
import os

input_folder = "./original_photos" 
output_folder = "./original_photos/new_photos"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        resized_img = cv2.resize(img, (320, 320))
        cv2.imwrite(os.path.join(output_folder, filename), resized_img)

print("Resizing complete!")

