import os
from PIL import Image

def rename_and_convert_files(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter out directories, we only want files
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]

    # Sort files to maintain consistent order (if needed)
    files.sort()

    # Start with an incrementing counter at 000
    counter = 0

    for file in files:
        # Get the file extension
        file_extension = os.path.splitext(file)[1].lower()

        # Define new filename with the increment starting at 000 (zero-padded)
        new_filename = f"team13_{counter:03}.jpg"  # Zero-padded 3 digits

        # Construct full file paths
        old_file_path = os.path.join(directory, file)
        new_file_path = os.path.join(directory, new_filename)

        # Open the image file, convert to 'RGB' if necessary, and save as .jpg
        try:
            with Image.open(old_file_path) as img:
                # Convert the image to RGB if it's not already (some formats like PNG have alpha channels)
                img = img.convert('RGB')
                img.save(new_file_path, 'JPEG')

            # Remove the old file (optional, to delete the original)
            os.remove(old_file_path)
            print(f"Renamed and converted: {file} -> {new_filename}")
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

        # Increment counter
        counter += 1

# Usage
directory_path = "./original_photos/new_photos"
rename_and_convert_files(directory_path)

