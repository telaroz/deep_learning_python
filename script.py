# pip install ultralytics fast_plate_ocr
from ultralytics import YOLO
from fast_plate_ocr import ONNXPlateRecognizer # https://github.com/ankandrew/fast-plate-ocr
import cv2
import os

# Detection model. It's a demo, we would have to create our own models
model = YOLO("https://github.com/ultralytics/assets/releases/download/v0.0.0/anpr-demo-model.pt")

image_path = "image1.jpg"
img = cv2.imread(image_path)
result = model.predict(img)

# One OCR model that exists and works. There are more and we can use multiple, so we have more confidence. 
ocr_model_fast = ONNXPlateRecognizer("global-plates-mobile-vit-v2-model")
detected_plates = []
temp_file_path = "temp.jpg"

YOLO(model="yolov8n.pt")

for box in result[0].boxes:
            # Get bounding box coordinates
            xyxy = box.xyxy[0].cpu().numpy().astype(int) # [xmin, ymin, xmax, ymax]
            confidence = box.conf[0].cpu().numpy()
            xmin, ymin, xmax, ymax = xyxy
            plate_crop = img[ymin:ymax,
                             xmin:xmax]
            
            # ONNX needs to have the image in a hard drive
            cv2.imwrite(temp_file_path, plate_crop)
            ocr_text_fast = ocr_model_fast.run(temp_file_path)
            os.remove(temp_file_path)

            detected_plates.append({
                "box": xyxy,
                "confidence": confidence,
                "fast_ocr": ocr_text_fast,
                "crop": plate_crop # Keep the crop for visualization
            })

            # --- Draw bounding box and OCR results on the original image ---
            label_fast = f"Fast: {ocr_text_fast}"
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2) # Green box
            # Position text labels above the box
            cv2.putText(img, label_fast, (xmin, ymin - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) # Red text

cv2.imwrite("output_annotated_image.jpg", img)
