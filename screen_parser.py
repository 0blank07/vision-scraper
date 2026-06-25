import cv2
import numpy as np
import easyocr
import os

class ScreenParser:
    def __init__(self):
        # Initialize EasyOCR reader (loads model into memory)
        print("Loading EasyOCR models... (this might take a few seconds on first run)")
        self.reader = easyocr.Reader(['en'], gpu=False) # Use CPU by default for broader compatibility
        
        # Base screen resolution for our hardcoded coordinates
        self.BASE_WIDTH = 1600
        self.BASE_HEIGHT = 900
        
        # Create image output directories
        os.makedirs("output/images/cards", exist_ok=True)
        os.makedirs("output/images/skills", exist_ok=True)
        os.makedirs("output/images/playstyles", exist_ok=True)
        os.makedirs("output/images/traits", exist_ok=True)

    def extract_text(self, img, bbox, allowlist=None):
        """
        Crop the image to the bounding box and perform OCR.
        bbox format: (x_start, y_start, x_end, y_end)
        """
        x1, y1, x2, y2 = bbox
        cropped = img[y1:y2, x1:x2]
        
        # Preprocessing to improve OCR accuracy on game fonts
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        
        # Optional: Apply thresholding if needed
        # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        results = self.reader.readtext(gray, allowlist=allowlist, detail=0)
        return " ".join(results).strip()

    def parse_summary_tab(self, img):
        """Extracts data from the Summary / Overview tab"""
        data = {}
        
        # Coordinates based on 1600x900 calibration
        data['first_name'] = self.extract_text(img, (440, 100, 700, 140))
        data['last_name'] = self.extract_text(img, (440, 140, 800, 200))
        data['bio_line'] = self.extract_text(img, (400, 210, 850, 250))
        
        data['position'] = self.extract_text(img, (200, 600, 260, 640))
        
        return data

    def crop_and_save_card_art(self, img, player_name):
        """Extract just the player card art without UI elements."""
        # Clean the name for filename
        clean_name = "".join([c for c in player_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        clean_name = clean_name.replace(" ", "_").lower()
        
        # Card art bounding box on the profile page
        # X: ~30 to 250, Y: ~100 to 500
        card_img = img[100:500, 30:250]
        filepath = f"output/images/cards/{clean_name}.png"
        cv2.imwrite(filepath, card_img)
        return filepath
