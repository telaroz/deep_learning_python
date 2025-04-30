from ultralytics import YOLO

data_yaml_path = 'datasets/data.yaml'

# Choose the model architecture (e.g., yolo11n.pt, yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt) Sizes here: https://docs.ultralytics.com/models/yolo11/#supported-tasks-and-modes

model_name = 'yolo11n.pt' # Using nano version for faster training --> 11x is bigger/better. 

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
