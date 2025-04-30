# convert_labels.py (Corrected Version)
import os
from PIL import Image # Install Pillow: pip install Pillow
import glob

# --- Configuration ---
SOURCE_LABEL_DIR = 'eu' # Directory containing your original .txt files
SOURCE_IMAGE_DIR = 'eu' # Directory containing your .jpg files
OUTPUT_LABEL_DIR = 'datasets/labels/unsplit' # Temporary output dir for converted labels
DEFAULT_YOLO_CLASS_ID = 0 # Assign this class ID to all detected objects
# --- End Configuration ---

os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

original_label_files = glob.glob(os.path.join(SOURCE_LABEL_DIR, '*.txt'))

print(f"Found {len(original_label_files)} original label files in {SOURCE_LABEL_DIR}")
print(f"Assigning default YOLO class ID: {DEFAULT_YOLO_CLASS_ID} to all detections.")

conversion_count = 0
error_count = 0

for txt_file_path in original_label_files:
    base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    # Assume corresponding image has the same base name
    image_file_path = os.path.join(SOURCE_IMAGE_DIR, base_name + '.jpg')
    output_txt_path = os.path.join(OUTPUT_LABEL_DIR, base_name + '.txt')

    if not os.path.exists(image_file_path):
        print(f"Warning: Image file not found for label '{txt_file_path}'. Expected at '{image_file_path}'. Skipping.")
        error_count += 1
        continue

    try:
        # Get image dimensions
        with Image.open(image_file_path) as img:
            img_width, img_height = img.size

        if img_width == 0 or img_height == 0:
             print(f"Warning: Image '{image_file_path}' has zero width or height. Skipping.")
             error_count += 1
             continue

        yolo_labels = []
        with open(txt_file_path, 'r') as f_in:
            lines = f_in.readlines()
            if not lines:
                print(f"Warning: Original label file '{txt_file_path}' is empty. Creating empty YOLO label file.")
                # Create an empty file to signify no objects
                open(output_txt_path, 'w').close()
                conversion_count +=1
                continue

            for line_num, line in enumerate(lines, 1):
                parts = line.strip().split()
                # Expecting at least 5 parts: img_name x_min y_min width height
                if len(parts) < 5:
                    print(f"Warning: Skipping malformed line #{line_num} in '{txt_file_path}' (expected >= 5 parts): {line.strip()}")
                    continue

                # Validate image name in the line matches the file name (optional but good practice)
                line_img_name = parts[0]
                if not line_img_name.lower().endswith('.jpg'):
                     print(f"Warning: Skipping line #{line_num} in '{txt_file_path}'. First part '{line_img_name}' doesn't look like an image name. Format assumed: <image_name.jpg> <x_min> <y_min> <width> <height> ...")
                     continue
                # Check if base name matches (optional, remove if names inside file can differ)
                # if os.path.splitext(line_img_name)[0] != base_name:
                #     print(f"Warning: Image name '{line_img_name}' in line #{line_num} of '{txt_file_path}' does not match file base name '{base_name}'. Processing anyway based on file name.")


                try:
                    # Coordinates start from the second element (index 1)
                    x_min = float(parts[1])
                    y_min = float(parts[2])
                    box_width = float(parts[3])
                    box_height = float(parts[4])

                    # Assign the default YOLO class ID
                    yolo_class_id = DEFAULT_YOLO_CLASS_ID

                    # Calculate center coordinates
                    x_center = x_min + box_width / 2
                    y_center = y_min + box_height / 2

                    # Normalize coordinates and dimensions
                    x_center_norm = x_center / img_width
                    y_center_norm = y_center / img_height
                    width_norm = box_width / img_width
                    height_norm = box_height / img_height

                    # Clamp values to [0.0, 1.0] just in case
                    x_center_norm = max(0.0, min(1.0, x_center_norm))
                    y_center_norm = max(0.0, min(1.0, y_center_norm))
                    width_norm = max(0.0, min(1.0, width_norm))
                    height_norm = max(0.0, min(1.0, height_norm))

                    yolo_labels.append(f"{yolo_class_id} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}")

                except ValueError:
                    print(f"Warning: Skipping line #{line_num} in '{txt_file_path}' due to non-numeric coordinate/dimension: {line.strip()}")
                    continue
                except Exception as e:
                     print(f"Warning: Error processing line #{line_num} in '{txt_file_path}': {line.strip()} - {e}")
                     continue

        # Write the converted labels to the new file
        if yolo_labels:
            with open(output_txt_path, 'w') as f_out:
                f_out.write("\n".join(yolo_labels))
            conversion_count += 1
        # Handle cases where the file had lines, but none were valid or converted
        elif not os.path.exists(output_txt_path):
             print(f"Warning: No valid annotations found in '{txt_file_path}' after conversion attempts. Creating empty YOLO label file.")
             open(output_txt_path, 'w').close()
             conversion_count +=1 # Still count as processed

    except FileNotFoundError:
        print(f"Error: Could not find image file: {image_file_path}")
        error_count += 1
    except Exception as e:
        print(f"Error processing file pair '{txt_file_path}' and '{image_file_path}': {e}")
        error_count += 1

print("-" * 20)
print(f"Label conversion finished.")
print(f"Successfully processed/converted: {conversion_count} label files")
print(f"Errors/Skipped files: {error_count} files")
print(f"Converted labels saved to: {OUTPUT_LABEL_DIR}")
print("-" * 20)
print(f"REMINDER: All objects were assigned the default class ID {DEFAULT_YOLO_CLASS_ID}. Ensure your data.yaml reflects this single class.")