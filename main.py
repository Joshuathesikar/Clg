import cv2
import numpy as np
import pandas as pd
import torch
import unicodedata
from ultralytics import YOLO
from license1 import extract_text_from_plate
from email1 import send_email

# Function to clean and normalize text (removes spaces, converts to uppercase, removes special characters)
def clean_text(text):
    return ''.join(c for c in str(text).strip().upper() if unicodedata.category(c)[0] != 'C' and c.isalnum())

# Load YOLO models (Ensure the paths are correct)
helmet_model = YOLO(r"C:\Users\LENOVO\Desktop\database\helmet\runs\detect\train\weights\best.pt")  
plate_model = YOLO(r"C:\Users\LENOVO\Desktop\database\runs\detect\train2\weights\best.pt")  

# Load vehicle-owner data (Ensure the CSV exists)
csv_data = pd.read_csv(r"C:\Users\LENOVO\Desktop\database\licenseplates.csv", encoding="utf-8")

# Standardize column names
csv_data.columns = [col.strip() for col in csv_data.columns]
csv_data['LicensePlate'] = csv_data['LicensePlate'].astype(str).apply(clean_text)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Stop if no frame is captured

    frame = cv2.flip(frame, 1)  # ✅ Fixes mirror effect (placed correctly here!)

    # Helmet detection
    helmet_results = helmet_model(frame, stream=True)  # Stream=True for proper handling
    
    no_helmet_detected = False
    for result in helmet_results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert tensor to list
            conf = float(box.conf[0])  # Confidence score
            cls = int(box.cls[0])  # Class ID
            
            print(f"🔍 Detected class: {cls}, Confidence: {conf:.2f}")  # Debugging

            label = "No Helmet" if cls == 1 else "Helmet"  # Adjust if needed
            color = (0, 0, 255) if cls == 1 else (0, 255, 0)  # Red for No Helmet, Green for Helmet
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if cls == 1:  # Adjust based on model output
                no_helmet_detected = True

    # License Plate Detection if No Helmet Found
    if no_helmet_detected:
        plate_results = plate_model(frame, stream=True)  # Stream=True for proper handling
        plates = []
        
        for result in plate_results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                plates.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, "License Plate", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Extract text from detected plates
        plate_numbers = extract_text_from_plate(frame, plates)

        for plate_number in plate_numbers:
            plate_number = clean_text(plate_number)
            print(f"🔍 Detected Plate: {plate_number}")

            # Check against the CSV data
            csv_data['LicensePlate'] = csv_data['LicensePlate'].astype(str).apply(clean_text)
            plate_number_cleaned = clean_text(plate_number)
            
            matches = csv_data[csv_data['LicensePlate'].str.contains(plate_number_cleaned, na=False, case=False)]

            if not matches.empty:
                if 'Email' in matches.columns:
                    owner_email = matches['Email'].values[0]
                    print(f"✅ Match Found: Sending email to {owner_email}")
                    send_email(owner_email, plate_number)
                else:
                    print("❌ 'Email' column missing in CSV!")
            else:
                print(f"❌ Plate not found! Searching for '{plate_number_cleaned}' in:")
                print(csv_data['LicensePlate'].tolist())

    # Show output frame
    cv2.imshow("Helmet & License Plate Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
