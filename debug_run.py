"""
Debug script: Takes a screenshot after EVERY single click so we can 
see exactly what screen we are on at each step.
"""
import time
from adb_controller import ADBController
from screen_parser import ScreenParser
import cv2

adb = ADBController()
parser = ScreenParser()

def shot(name):
    adb.get_screenshot()
    img = cv2.imread("temp.png")
    cv2.imwrite(f"debug_steps/{name}.png", img)
    print(f"  >> Screenshot saved: debug_steps/{name}.png")
    return img

import os
os.makedirs("debug_steps", exist_ok=True)

print("=== STEP 1: Taking initial screenshot (should be Home) ===")
shot("01_home")

print("=== STEP 2: Clicking SIGNINGS (800, 850) ===")
adb.click(800, 850)
time.sleep(3)
shot("02_after_signings")

print("=== STEP 3: Clicking Search button (240, 760) ===")
adb.click(240, 760)
time.sleep(2)
shot("03_after_search_btn")

print("=== STEP 4: Clicking MIN OVR box (520, 370), typing 120 ===")
adb.click(520, 370)
time.sleep(0.5)
adb._run_cmd(["adb", "-s", adb.device_id, "shell", "input", "text", "120"])
time.sleep(0.5)

print("=== STEP 5: Clicking MAX OVR box (690, 370), typing 120 ===")
adb.click(690, 370)
time.sleep(0.5)
adb._run_cmd(["adb", "-s", adb.device_id, "shell", "input", "text", "120"])
time.sleep(0.5)
shot("04_after_ovr_input")

print("=== STEP 6: Closing keyboard (BACK key) ===")
adb._run_cmd(["adb", "-s", adb.device_id, "shell", "input", "keyevent", "4"])
time.sleep(0.5)

print("=== STEP 7: Clicking SEARCH submit (1100, 825) ===")
adb.click(1100, 825)
print("  Waiting 7 seconds for results to load...")
time.sleep(7)
img7 = shot("05_after_search_submit")

# Check for and dismiss error popups
print("=== STEP 8: Checking for error popups ===")
for i in range(20):
    img = cv2.imread("temp.png")
    text = parser.extract_text(img, (200, 200, 1400, 700))
    if "UNKNOWN" in text or "token" in text.lower() or "Error at line" in text:
        print(f"  [{i+1}] Error detected! Clicking OK (800, 600)...")
        adb.click(800, 600)
        time.sleep(3)
        shot(f"05b_after_ok_dismiss_{i+1}")
    else:
        print("  Screen clear of errors!")
        break

shot("06_results_grid")

print("=== STEP 9: Clicking 1st player card (390, 350) ===")
adb.click(390, 350)
time.sleep(4)  # Wait for side panel to open
shot("07_after_1st_player_click")

print("=== STEP 10: Clicking side panel card (1350, 450) ===")
adb.click(1350, 450)
time.sleep(5)  # Wait for profile to open
shot("08_after_side_panel_click")

print("\n=== ALL DONE - check debug_steps/ folder for screenshots ===")
print("The key ones to look at are:")
print("  06_results_grid.png    - what the search results look like")
print("  07_after_1st_player_click.png - did the side panel open?")
print("  08_after_side_panel_click.png - did the player profile open?")
