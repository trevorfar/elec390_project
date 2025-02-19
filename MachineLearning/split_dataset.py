import os
import random
import shutil
import lxml.etree as ET

def clean_xml_file(xml_path):
    """ Reads an XML file, removes encoding declaration, and rewrites it. """
    if not os.path.exists(xml_path):
        print(f"Warning: Annotation file not found {xml_path}")
        return False  # Return False if the XML file is missing

    with open(xml_path, "rb") as f:  # Read as bytes
        xml_bytes = f.read()

    try:
        # Parse the XML while ensuring it's valid
        xml_tree = ET.fromstring(xml_bytes)

        # Convert back to string without encoding declaration
        clean_xml = ET.tostring(xml_tree, pretty_print=True, encoding="utf-8", xml_declaration=False)

        # Overwrite the original file
        with open(xml_path, "wb") as f:
            f.write(clean_xml)

        return True  # Indicate successful cleaning

    except ET.XMLSyntaxError:
        print(f"Error parsing XML file: {xml_path}, skipping...")
        return False  # Return False if XML is invalid

def split_dataset(images_path, annotations_path, val_split, test_split, out_path):
    """Splits a directory of sorted images/annotations into training, validation, and test sets."""

    train_dir = os.path.join(out_path, 'train')
    val_dir = os.path.join(out_path, 'validation')
    test_dir = os.path.join(out_path, 'test')

    IMAGES_TRAIN_DIR = os.path.join(train_dir, 'images')
    IMAGES_VAL_DIR = os.path.join(val_dir, 'images')
    IMAGES_TEST_DIR = os.path.join(test_dir, 'images')
    os.makedirs(IMAGES_TRAIN_DIR, exist_ok=True)
    os.makedirs(IMAGES_VAL_DIR, exist_ok=True)
    os.makedirs(IMAGES_TEST_DIR, exist_ok=True)

    ANNOT_TRAIN_DIR = os.path.join(train_dir, 'annotations')
    ANNOT_VAL_DIR = os.path.join(val_dir, 'annotations')
    ANNOT_TEST_DIR = os.path.join(test_dir, 'annotations')
    os.makedirs(ANNOT_TRAIN_DIR, exist_ok=True)
    os.makedirs(ANNOT_VAL_DIR, exist_ok=True)
    os.makedirs(ANNOT_TEST_DIR, exist_ok=True)

    # Get all filenames for this dir, filtered by filetype
    filenames = [f for f in os.listdir(images_path) if f.endswith('.jpg')]
    filenames.sort()
    random.seed(42)
    random.shuffle(filenames)

    val_count = int(len(filenames) * val_split)
    test_count = int(len(filenames) * test_split)

    for i, filename in enumerate(filenames):
        image_file = os.path.join(images_path, filename)
        annot_file = os.path.join(annotations_path, filename.replace("jpg", "xml"))

        if not os.path.exists(image_file):
            print(f"Warning: Image file {image_file} not found, skipping.")
            continue

        if clean_xml_file(annot_file):  # Ensure XML is valid before copying
            if i < val_count:
                shutil.copy(image_file, IMAGES_VAL_DIR)
                shutil.copy(annot_file, ANNOT_VAL_DIR)
            elif i < val_count + test_count:
                shutil.copy(image_file, IMAGES_TEST_DIR)
                shutil.copy(annot_file, ANNOT_TEST_DIR)
            else:
                shutil.copy(image_file, IMAGES_TRAIN_DIR)
                shutil.copy(annot_file, ANNOT_TRAIN_DIR)
        else:
            print(f"Skipping {annot_file} due to XML errors.")

    return (train_dir, val_dir, test_dir)

