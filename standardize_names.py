import os
import glob
import re # For sorting

TARGET_DIR = 'eu' # The directory containing files to rename

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

# Find all image files 
image_files = glob.glob(os.path.join(TARGET_DIR, '*.jpg'))

base_names = [os.path.splitext(os.path.basename(f))[0] for f in image_files]

# Sort the base names
base_names.sort(key=natural_sort_key)


# Renaming Phase

# We go through the sorted list and assign new sequential eu_XXX names
for i, old_base in enumerate(base_names, 1):
    new_base = f"eu_{i:03d}" # Format as eu_001, eu_002, ...

    # Define old and new paths
    old_img_path = os.path.join(TARGET_DIR, old_base + ".jpg")
    old_txt_path = os.path.join(TARGET_DIR, old_base + ".txt")
    new_img_path = os.path.join(TARGET_DIR, new_base + ".jpg")
    new_txt_path = os.path.join(TARGET_DIR, new_base + ".txt")

    os.rename(old_img_path, new_img_path)
    os.rename(old_txt_path, new_txt_path)
