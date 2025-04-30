from ultralytics import YOLO

data_yaml_path = 'datasets/data.yaml'

# Choose the model architecture (e.g., yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8x.pt)

model_name = 'yolov8n.pt' # Using nano version for faster training --> 8x is bigger/better

model = YOLO(model_name)

# Training hyperparameters
EPOCHS = 2       
IMG_SIZE = 640    
BATCH_SIZE = 16   
PATIENCE = 5

results = model.train(
            data = data_yaml_path,
            epochs = EPOCHS,
            imgsz = IMG_SIZE,
            batch = BATCH_SIZE,
            patience = PATIENCE)

print(f"Results saved to: runs/detect/train")
