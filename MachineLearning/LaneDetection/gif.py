from PIL import Image
import os

image_dir = 'output_images' 
output_gif = 'output_gif.gif'

filenames = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

filenames.sort()

images = []
for filename in filenames:
    img = Image.open(filename)
    img = img.resize((640, 480))  # Resize to 640x480
    images.append(img)

images[0].save(
    output_gif,
    save_all=True,
    append_images=images[1:],
    duration=1000,  # 1000 ms = 1 second per frame
    loop=1,  # 0 means infinite loop
)

print(f"GIF saved as {output_gif}")
