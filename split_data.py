# split_data.py
import os
import glob
import random
import shutil

SOURCE_IMAGE_DIR = 'eu' # Where your original .jpg images are
SOURCE_CONVERTED_LABEL_DIR = 'datasets/labels/unsplit' # Where the converted labels are
DEST_BASE_DIR = 'datasets' # Base directory for final structure
TRAIN_RATIO = 0.8

# Create destination directories
train_img_dir = os.path.join(DEST_BASE_DIR, 'images', 'train')
val_img_dir = os.path.join(DEST_BASE_DIR, 'images', 'val')
train_lbl_dir = os.path.join(DEST_BASE_DIR, 'labels', 'train')
val_lbl_dir = os.path.join(DEST_BASE_DIR, 'labels', 'val')

os.makedirs(train_img_dir)
os.makedirs(val_img_dir)
os.makedirs(train_lbl_dir)
os.makedirs(val_lbl_dir)

# Get all image files
image_files = glob.glob(os.path.join(SOURCE_IMAGE_DIR, '*.jpg'))

# Shuffle the files
random.shuffle(image_files)

# Calculate split index
split_index = int(len(image_files) * TRAIN_RATIO)

# Split into train and validation sets
train_files = image_files[:split_index]
val_files = image_files[split_index:]



# Function to move files
for img_path in file_list:
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    lbl_name = base_name + '.txt'
    src_lbl_path = os.path.join(SOURCE_CONVERTED_LABEL_DIR, lbl_name)
    dest_img_path = os.path.join(dest_img_dir, os.path.basename(img_path))
    dest_lbl_path = os.path.join(dest_lbl_dir, lbl_name)
    shutil.move(img_path, dest_img_path)
    shutil.move(src_lbl_path, dest_lbl_path)


os.rmdir(SOURCE_CONVERTED_LABEL_DIR)
