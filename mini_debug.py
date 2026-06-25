import time
from adb_controller import ADBController
from screen_parser import ScreenParser
import cv2
import os

adb = ADBController()
parser = ScreenParser()
os.makedirs("debug_steps", exist_ok=True)

def shot(name):
    img_np = adb.get_screenshot()
    if img_np is not None:
        cv2.imwrite(f"debug_steps/{name}.png", img_np)
        print(f"  >> Screenshot saved: debug_steps/{name}.png")
    return img_np

print("=== STEP 1: Initial state (Should be Home) ===")
shot("01_initial")

print("=== STEP 2: Clicking SIGNINGS (808, 844) ===")
adb.click(808, 844)
time.sleep(4)
shot("02_after_signings")

print("=== STEP 3: Clicking Search button (240, 760) ===")
adb.click(240, 760)
time.sleep(2)
shot("03_after_search")

print("=== DONE ===")
