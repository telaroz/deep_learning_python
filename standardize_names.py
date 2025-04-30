import os
import glob
import re # For natural sorting

# --- Configuration ---
TARGET_DIR = 'eu' # The directory containing files to rename
# --- End Configuration ---

def natural_sort_key(s):
    """
    Key for natural sorting (e.g., 'image1', 'image2', 'image10').
    Splits string into text and number parts.
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

print(f"Scanning directory: {TARGET_DIR} for renaming to eu_XXX format.")

# Find all image files (we'll use these to determine the order)
image_files = glob.glob(os.path.join(TARGET_DIR, '*.jpg'))

if not image_files:
    print("No .jpg files found in the directory. Exiting.")
    exit()

# Extract base names (filename without extension)
base_names = [os.path.splitext(os.path.basename(f))[0] for f in image_files]

# Sort the base names naturally
base_names.sort(key=natural_sort_key)

print(f"Found {len(base_names)} base names to process.")
print("Renaming order will be based on this sorted list:")
for i, name in enumerate(base_names):
     print(f"  {i+1}: {name}")
print("-" * 20)


renamed_count = 0
skipped_count = 0
error_count = 0
missing_txt_count = 0

# --- Renaming Phase ---
# We iterate through the sorted list and assign new sequential eu_XXX names
for i, old_base in enumerate(base_names, 1):
    new_base = f"eu_{i:03d}" # Format like eu_001, eu_002, ...

    # Define old and new paths
    old_img_path = os.path.join(TARGET_DIR, old_base + ".jpg")
    old_txt_path = os.path.join(TARGET_DIR, old_base + ".txt")
    new_img_path = os.path.join(TARGET_DIR, new_base + ".jpg")
    new_txt_path = os.path.join(TARGET_DIR, new_base + ".txt")

    # Skip if the file is already named correctly (unlikely in this full rename scenario, but safe)
    if old_base == new_base:
        print(f"Skipping: '{old_base}' is already in the target format.")
        skipped_count += 1
        continue

    # --- Rename Image File ---
    img_renamed = False
    if os.path.exists(old_img_path):
         # Safety Check: Ensure the target path doesn't already exist unexpectedly
        if os.path.exists(new_img_path):
            print(f"Error: Target image path '{new_img_path}' already exists! Cannot rename '{old_img_path}'. Skipping this pair.")
            error_count += 1
            continue # Skip both image and text for this pair
        try:
            os.rename(old_img_path, new_img_path)
            print(f"Renamed IMG: '{old_base}.jpg' -> '{new_base}.jpg'")
            renamed_count += 1
            img_renamed = True
        except OSError as e:
            print(f"Error renaming image '{old_base}.jpg': {e}")
            error_count += 1
            continue # Skip text file if image rename failed
    else:
        # This shouldn't happen if we sourced from existing jpgs, but check anyway
        print(f"Warning: Original image file '{old_img_path}' not found during renaming phase. Skipping.")
        error_count += 1
        continue

    # --- Rename Text File (if it exists) ---
    if os.path.exists(old_txt_path):
        # Safety Check: Ensure the target path doesn't already exist unexpectedly
        if os.path.exists(new_txt_path):
             print(f"Error: Target text path '{new_txt_path}' already exists! Cannot rename '{old_txt_path}'.")
             error_count += 1
             # Note: The image might have been renamed successfully above
        else:
            try:
                os.rename(old_txt_path, new_txt_path)
                print(f"Renamed TXT: '{old_base}.txt' -> '{new_base}.txt'")
                # Don't double-increment renamed_count, just track success
            except OSError as e:
                print(f"Error renaming text file '{old_base}.txt': {e}")
                error_count += 1
    elif img_renamed: # Only report missing text if the image existed and was renamed
        print(f"Info: Corresponding text file '{old_txt_path}' not found for image '{new_base}.jpg'.")
        missing_txt_count += 1


print("-" * 20)
print("Universal renaming finished.")
print(f"Image/Text pairs processed for renaming: {len(base_names)}")
print(f"Files renamed (counting images): {renamed_count}")
print(f"Pairs skipped (already correct format): {skipped_count}")
print(f"Missing corresponding .txt files: {missing_txt_count}")
print(f"Errors encountered: {error_count}")
print("-" * 20)
print(f"All files in '{TARGET_DIR}' should now follow the 'eu_XXX' format.")