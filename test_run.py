from screen_parser import ScreenParser
import cv2
import json

parser = ScreenParser()
img = cv2.imread('attributes.png')
with open('bounding_boxes.json') as f:
    bboxes = json.load(f)
bbox = bboxes['attributes']
print('Box:', bbox)
text = parser.extract_text(img, bbox=bbox)
print('Text:', text)
attrs = parser.parse_attributes(text)
print('Parsed Attributes:', attrs)
