import os
import xml.etree.ElementTree as ET
from collections import Counter

def count_labels_in_xml():
    label_counts = Counter()
    
    path = "./dataset/Annotations"  # Make sure this directory exists
    
    if not os.path.exists(path):
        print(f"Error: Directory '{path}' not found.")
        return
    
    for file in os.listdir(path):
        if file.endswith(".xml"):
            file_path = os.path.join(path, file)  # Use full file path
            try:
                tree = ET.parse(file_path)  # Use the full path here
                root = tree.getroot()
                
                for obj in root.findall(".//object/name"):
                    label = obj.text.strip()
                    label_counts[label] += 1
            except ET.ParseError:
                print(f"Error parsing {file}")
            except Exception as e:
                print(f"Unexpected error with {file}: {e}")
    
    # Print the count of each unique label
    for label, count in label_counts.items():
        print(f"{label}: {count}")

if __name__ == "__main__":
    count_labels_in_xml()

