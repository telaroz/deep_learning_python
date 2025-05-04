# pip install ultralytics fast_plate_ocr pytesseract easyocr
from ultralytics import YOLO
from fast_plate_ocr import ONNXPlateRecognizer # https://github.com/ankandrew/fast-plate-ocr
import pytesseract
import easyocr 
import cv2
import os

# Detection model. It's a demo, we would have to create our own models

print("Select Detection Model: \n 1: ANPR_DEMO_MODEL \n 2: MODEL1 \n 3: MODEL2")

detection_model_choice = int(input("Enter choice (1, 2, or 3): "))


if detection_model_choice == 1:
    model_path = "models/anpr-demo-model.pt"
elif detection_model_choice == 2:
    model_path = "models/model1.pt"
elif detection_model_choice == 3:
    model_path = "models/model2.pt"
else:
    print("Invalid choice, using default: models/anpr-demo-model.pt")
    model_path = "models/anpr-demo-model.pt" # Default fallback

model = YOLO(model_path)    

print("\nSelect OCR Model: \n 1: ONNXPlateRecognizer (Fast Plate OCR) \n 2: Pytesseract \n 3: EasyOCR")

ocr_model_choice = int(input("Enter choice (1, 2, or 3): "))

image_path = input("Enter which image in the project directory you want to detect Plates from: ")
if not os.path.exists(image_path):
    print(f"Error: File not found at '{image_path}'. Please check the path and filename.")
    image_path = input("Try entering the path again: ")

img = cv2.imread(image_path)
result = model.predict(img)


detected_plates = []
temp_file_path = "temp.jpg"

for box in result[0].boxes:
    # Get bounding box coordinates
    xyxy = box.xyxy[0].cpu().numpy().astype(int) # [xmin, ymin, xmax, ymax]
    confidence = box.conf[0].cpu().numpy()
    xmin, ymin, xmax, ymax = xyxy
    plate_crop = img[ymin:ymax,
                     xmin:xmax]

    if ocr_model_choice == 1:
        # ONNX needs to have the image in a hard drive
        ocr_method_name = "ONNXPlateRecognizer"
        cv2.imwrite(temp_file_path, plate_crop)
        ocr_model_fast = ONNXPlateRecognizer("global-plates-mobile-vit-v2-model")
        ocr_text = ocr_model_fast.run(temp_file_path)
        os.remove(temp_file_path)

    elif ocr_model_choice == 2:
        # For pytesseract
        ocr_method_name = "Pytesseract"
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ocr_text = pytesseract.image_to_string(plate_crop, config=custom_config).strip()

    elif ocr_model_choice == 3:
        # For easyOCR
        ocr_method_name = "EasyOCR"
        ocr_easy_model = easyocr.Reader(['en'], gpu=True)
        ocr_results_list = ocr_easy_model.readtext(plate_crop)
        ocr_text = " ".join([res[1] for res in ocr_results_list]).strip()

    detected_plates.append({
        "box": xyxy,
        "confidence": confidence,
        "OCR_result": ocr_text,
        "crop": plate_crop # Keep the crop for visualization
    })

    # --- Draw bounding box and OCR results on the original image ---
    label_fast = f"Fast: {ocr_text}"
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2) # Green box
    # Position text labels above the box
    cv2.putText(img, label_fast, (xmin, ymin - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) # Red text

cv2.imwrite("output_annotated_image.jpg", img)

for i, plate_info in enumerate(detected_plates):
    plate_number = plate_info['OCR_result'] if plate_info['OCR_result'] else "[OCR Failed]"
    print(f"Plate {i + 1}: {plate_number} (Confidence of the plate detection: {plate_info['confidence']:.2f})")