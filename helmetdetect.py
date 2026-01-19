import cv2
import torch
from ultralytics import YOLO

# Load trained YOLOv8 model
helmet_model = YOLO("C:\Users\LENOVO\Desktop\database\helmet\runs\detect\train\weights\best.pt")

# Open webcam or video file
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = helmet_model(frame)

    no_helmet_detected = False
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box.tolist()
            if int(cls) == 0:  # Class 0 = No Helmet
                no_helmet_detected = True
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                cv2.putText(frame, "No Helmet!", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if no_helmet_detected:
        detect_number_plate(frame)  # Call number plate detection module

    cv2.imshow("Helmet Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
