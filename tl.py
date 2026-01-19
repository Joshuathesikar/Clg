from ultralytics import YOLO

model = YOLO("yolov8s.pt")  # Start with a pre-trained model
model.train(
    data="C:/Users/LENOVO/Desktop/database/license/data2.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu"  # Force CPU mode
)

model.export(format="pt")  # Save trained model
