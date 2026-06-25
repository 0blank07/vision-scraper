import cv2
import numpy as np
import easyocr
import os
import re

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

    def preprocess_image(self, img):
        """Applies grayscale and contrast enhancement to fix game UI OCR issues."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(gray)

    def extract_text(self, img, bbox=None, allowlist=None):
        """
        Crop the image to the bounding box and perform OCR with preprocessing.
        If bbox is None, performs OCR on the entire image.
        bbox format: (x_start, y_start, x_end, y_end)
        """
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            # Ensure coordinates are within image bounds
            h, w = img.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            cropped = img[y1:y2, x1:x2]
        else:
            cropped = img
        
        processed = self.preprocess_image(cropped)
        results = self.reader.readtext(processed, allowlist=allowlist, detail=0)
        return " ".join(results).strip()

    def parse_attributes(self, text):
        """Regex parser to find 'AttributeName 123' patterns in the text."""
        # Matches words (Starting with Capital) followed by space and numbers
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s+(\d{1,3})'
        matches = re.findall(pattern, text)
        
        attributes = {}
        for attr, val in matches:
            # Clean up common easyOCR hallucination on game fonts
            attr = attr.replace('ppribbling', 'Dribbling').replace('Jumpingg', 'Jumping').strip()
            attributes[attr] = int(val)
        return attributes

    def parse_skill_boosts(self, text):
        """Regex parser to find 'AttributeName +10' patterns in skill popups."""
        # Matches words followed by a plus sign and numbers
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s*\+\s*(\d{1,3})'
        matches = re.findall(pattern, text)
        
        boosts = {}
        for attr, val in matches:
            attr = attr.replace('ppribbling', 'Dribbling').strip()
            boosts[attr] = f"+{val}"
        return boosts
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
