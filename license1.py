import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_plate(image, plates):
    plate_texts = []

    for (x1, y1, x2, y2) in plates:
        plate_img = image[y1:y2, x1:x2]

        # ✅ Convert to grayscale for better contrast
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

        # ✅ Apply adaptive thresholding for different lighting conditions
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 15, 8)

        # ✅ Reduce noise using morphological transformations
        kernel = np.ones((2,2), np.uint8)
        processed_img = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

        # ✅ Increase sharpness
        processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)

        # ✅ Try different OCR settings
        custom_config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        plate_text = pytesseract.image_to_string(processed_img, config=custom_config)

        plate_text = plate_text.strip().upper()  # Standardize text

        if plate_text:
            plate_texts.append(plate_text)

    return plate_texts
