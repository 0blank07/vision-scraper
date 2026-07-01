import cv2
import numpy as np
import easyocr
import os
import re
import difflib
from dictionaries import SKILL_SIGNATURES, PLAYSTYLES

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
        
        # Production Ground-Truth Dictionary for Fuzzy Matching
        self.VALID_ATTRIBUTES = [
            "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical",
            "Acceleration", "Sprint Speed", "Positioning", "Finishing", "Shot Power", 
            "Long Shot", "Volley", "Penalties", "Vision", "Crossing", "Free Kick", 
            "Short Passing", "Long Passing", "Curve", "Agility", "Balance", 
            "Reactions", "Ball Control", "Interceptions", "Heading", "Awareness", 
            "Stand Tackle", "Standing Tackle", "Sliding Tackle", "Jumping", "Strength", "Aggression", "Marking",
            "Diving", "Positioning", "Handling", "Reflexes", "Kicking"
        ]

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
        
        # ATTEMPT 1: Standard CLAHE Preprocessing
        processed = self.preprocess_image(cropped)
        results = self.reader.readtext(processed, allowlist=allowlist, detail=0)
        text = " ".join(results).strip()
            
        return text

    def parse_attributes(self, text):
        """Regex parser to find 'AttributeName 123' patterns in the text."""
        import difflib
        import re
        
        # Matches words (case-insensitive) followed by optional space/colon/dash and numbers
        pattern = r'([a-zA-Z]+(?:\s[a-zA-Z]+)*)\s*[:\-]?\s*(\d{2,3})'
        matches = re.findall(pattern, text)
        
        attributes = {}
        for attr, val in matches:
            attr = attr.strip()
            
            # Fuzzy match against the known valid attributes to auto-correct OCR errors
            closest = difflib.get_close_matches(attr, self.VALID_ATTRIBUTES, n=1, cutoff=0.5)
            final_attr = closest[0] if closest else attr.title()
            
            # Prevent sub-categories from deleting main categories
            if final_attr in attributes:
                attributes[f"{final_attr}_Stat"] = int(val)
            else:
                attributes[final_attr] = int(val)
        return attributes

    def parse_skill_boosts(self, text):
        """Regex parser to find 'AttributeName +10' patterns in skill popups."""
        import difflib
        import re
        
        # Matches words followed by an optional plus sign and numbers
        pattern = r'([a-zA-Z]+(?:\s[a-zA-Z]+)*)\s*\+?\s*(\d{1,3})'
        matches = re.findall(pattern, text)
        
        boosts = {}
        positions = []
        
        for attr, val in matches:
            # FIX 3: Ignore +0 boosts
            if val == "0":
                continue
                
            attr = attr.strip()
            lower_attr = attr.lower()
            
            # FIX 4: Filter out "Ovr" completely
            if lower_attr == "ovr":
                continue
            
            # FIX 1: Filter out "Unlocks after..." or "... Reaches Lvl" strings
            if "unlock" in lower_attr or "reach" in lower_attr or "lvl" in lower_attr:
                continue
                
            # FIX 2: Handle garbled "Position Lm Position Cam Aggression"
            # Extract all "Position <Pos>" and remove them from the attr string
            pos_matches = re.findall(r'(?i)position\s+([a-zA-Z]{2,3})', attr)
            for pos in pos_matches:
                positions.append(pos.title())
                
            # Remove the matched positions and the word 'Position' from the attribute name
            attr = re.sub(r'(?i)position\s+[a-zA-Z]{2,3}', '', attr).strip()
            
            # If the attribute is now empty (e.g. it was just positions), skip it
            if not attr:
                continue
            
            # Known OCR cutoff overrides
            if attr.lower() == "shot": attr = "Long Shot"
            elif attr.lower() == "tackle": attr = "Standing Tackle"
            elif attr.lower() == "passing": attr = "Short Passing"
            
            # Fuzzy match to production dictionary
            closest = difflib.get_close_matches(attr, self.VALID_ATTRIBUTES, n=1, cutoff=0.6)
            final_attr = closest[0] if closest else attr.title()
            
            # Add to boosts (avoids OCR duplicate glitches overwriting)
            if final_attr not in boosts:
                boosts[final_attr] = f"+{val}"
                
        # Handle positions list
        if positions:
            # Deduplicate in case OCR caught it multiple times
            unique_positions = list(dict.fromkeys(positions))
            # Standard JSON cannot have duplicate keys like `"Position": "Lm", "Position": "Cam"`
            # so we store it as a list array: `"Positions": ["Lm", "Cam"]`
            boosts["Positions"] = unique_positions
            
        return boosts

    def reverse_engineer_skill(self, boosts_dict):
        """Identifies the skill name perfectly by matching the combination of boosted stats."""
        # Filter out random junk like 'Ovr' or 'Unlocks After Wingback...'
        clean_stats = []
        for k in boosts_dict.keys():
            if k in self.VALID_ATTRIBUTES:
                clean_stats.append(k)
        
        sig = "|".join(sorted(clean_stats)).lower()
        if sig in SKILL_SIGNATURES:
            return SKILL_SIGNATURES[sig]["name"].upper()
        return ""

    def reverse_engineer_playstyle(self, raw_name, raw_level):
        """Matches a messy OCR playstyle name to a real one, and returns perfect name + description + level."""
        closest = difflib.get_close_matches(raw_name.upper(), PLAYSTYLES.keys(), n=1, cutoff=0.4)
        final_name = closest[0] if closest else raw_name
        
        # Level is always Lvl1 or Lvl2
        level = "Lvl 1" if "1" in str(raw_level) or "l" in str(raw_level).lower() else "Lvl 2"
        if "2" in str(raw_level): level = "Lvl 2"
        
        desc = PLAYSTYLES.get(final_name, "")
        
        return {
            "playstyle_name": final_name,
            "playstyle_level": level,
            "playstyle_description": desc
        }

    def clean_preferred_foot(self, raw_str):
        """Extracts exactly 2 digits representing weak and strong foot from OCR."""
        nums = re.findall(r'\d', raw_str)
        if len(nums) >= 2:
            return nums[0] + nums[1]
        return ""

    def parse_summary(self, img):
        """Extracts data from the Summary / Overview tab"""
        data = {}
        
        # Coordinates based on 1600x900 calibration
        data['first_name'] = self.extract_text(img, (440, 100, 700, 140))
        data['last_name'] = self.extract_text(img, (440, 140, 800, 200))
        data['bio_line'] = self.extract_text(img, (400, 210, 850, 250))
        
        data['position'] = self.extract_text(img, (200, 600, 260, 640))
        
        return data

    def count_stars(self, img, bbox=None):
        """Count gold stars in a bounding box using HSV color filtering"""
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            h, w = img.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            cropped = img[y1:y2, x1:x2]
        else:
            cropped = img
            
        # Convert to HSV color space
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        
        # Define range of gold/yellow color in HSV
        lower_gold = np.array([15, 100, 100])
        upper_gold = np.array([45, 255, 255])
        
        # Create a mask of the gold pixels
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        
        # Find continuous shapes (contours) in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter out tiny noise and count actual stars
        star_count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10:  # Minimum pixel area to be considered a star
                star_count += 1
                
        return star_count

    def crop_and_save(self, img, bbox, filepath):
        """Crops the image to the bbox and saves it"""
        if bbox is None:
            return None
        x1, y1, x2, y2 = bbox
        h, w = img.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        cropped = img[y1:y2, x1:x2]
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        cv2.imwrite(filepath, cropped)
        return filepath
