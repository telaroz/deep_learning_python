# split_data.py
import os
import glob
import random
import shutil

# --- Configuration ---
SOURCE_IMAGE_DIR = 'eu' # Where your original .jpg images are
SOURCE_CONVERTED_LABEL_DIR = 'datasets/labels/unsplit' # Where the converted labels are
DEST_BASE_DIR = 'datasets' # Base directory for final structure
TRAIN_RATIO = 0.8 # 80% for training, 20% for validation
# --- End Configuration ---

# Create destination directories
train_img_dir = os.path.join(DEST_BASE_DIR, 'images', 'train')
val_img_dir = os.path.join(DEST_BASE_DIR, 'images', 'val')
train_lbl_dir = os.path.join(DEST_BASE_DIR, 'labels', 'train')
val_lbl_dir = os.path.join(DEST_BASE_DIR, 'labels', 'val')

os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(val_img_dir, exist_ok=True)
os.makedirs(train_lbl_dir, exist_ok=True)
os.makedirs(val_lbl_dir, exist_ok=True)

# Get all image files
image_files = glob.glob(os.path.join(SOURCE_IMAGE_DIR, '*.jpg'))
print(f"Found {len(image_files)} image files.")

# Shuffle the files randomly
random.shuffle(image_files)

# Calculate split index
split_index = int(len(image_files) * TRAIN_RATIO)

# Split into train and validation sets
train_files = image_files[:split_index]
val_files = image_files[split_index:]

print(f"Splitting into {len(train_files)} training and {len(val_files)} validation samples.")

moved_train_count = 0
moved_val_count = 0
error_count = 0

# Function to move files
def move_files(file_list, dest_img_dir, dest_lbl_dir):
    count = 0
    errors = 0
    for img_path in file_list:
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        lbl_name = base_name + '.txt'
        src_lbl_path = os.path.join(SOURCE_CONVERTED_LABEL_DIR, lbl_name)

        dest_img_path = os.path.join(dest_img_dir, os.path.basename(img_path))
        dest_lbl_path = os.path.join(dest_lbl_dir, lbl_name)

        # Check if converted label exists before moving image
        if os.path.exists(src_lbl_path):
            try:
                shutil.move(img_path, dest_img_path)
                shutil.move(src_lbl_path, dest_lbl_path)
                count += 1
            except Exception as e:
                print(f"Error moving file pair for {base_name}: {e}")
                errors += 1
        else:
            print(f"Warning: Converted label file '{src_lbl_path}' not found. Skipping image '{img_path}'.")
            # Optionally: copy the image anyway if you want images without labels in your set
            # try:
            #     shutil.copy(img_path, dest_img_path)
            #     # Create empty label file? Or handle missing labels during training.
            #     open(dest_lbl_path, 'w').close() # Creates empty label file
            #     count += 1 # Count if copied
            # except Exception as e:
            #      print(f"Error copying image file {base_name}: {e}")
            #      errors += 1
            errors += 1 # Count as error if skipping

    return count, errors

# Move training files
print("\nMoving training files...")
moved_train, train_errors = move_files(train_files, train_img_dir, train_lbl_dir)
moved_train_count += moved_train
error_count += train_errors

# Move validation files
print("\nMoving validation files...")
moved_val, val_errors = move_files(val_files, val_img_dir, val_lbl_dir)
moved_val_count += moved_val
error_count += val_errors

print("-" * 20)
print("Data splitting and moving finished.")
print(f"Moved {moved_train_count} training image/label pairs.")
print(f"Moved {moved_val_count} validation image/label pairs.")
print(f"Encountered {error_count} errors/skipped files.")
print(f"Dataset organized in: {DEST_BASE_DIR}")
print("-" * 20)

# Optional: Clean up the temporary unsplit labeladirectory
try:
    if not os.listdir(SOURCE_CONVERTED_LABEL_DIR): # Only remove if empty
        os.rmdir(SOURCE_CONVERTED_LABEL_DIR)
        print(f"Removed empty temporary directory: {SOURCE_CONVERTED_LABEL_DIR}")
    else:
         print(f"Warning: Temporary directory {SOURCE_CONVERTED_LABEL_DIR} not empty. Manual cleanup might be needed.")
except OSError as e:
    print(f"Could not remove temporary directory {SOURCE_CONVERTED_LABEL_DIR}: {e}")