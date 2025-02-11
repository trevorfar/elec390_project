from PIL import Image
import os

# Input and output folders
input_folder = "./original_photos/new_photos"  # Change this to your image folder
output_folder = "./original_photos/new_photos"
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(input_folder, filename)

        img = Image.open(img_path).convert("RGB")

        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(output_folder, jpg_filename)
        img.save(jpg_path, "JPEG", quality=95)



