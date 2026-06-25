import subprocess
import time
import cv2
import numpy as np

class ADBController:
    def __init__(self, device_id="emulator-5554"):
        self.device_id = device_id
        # Ensure device is connected
        self._run_cmd(["adb", "devices"])

    def _run_cmd(self, cmd):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ADB Error: {result.stderr}")
        return result.stdout

    def click(self, x, y):
        """Send a tap event at specific coordinates using a 100ms swipe to ensure the game engine registers it."""
        print(f"Clicking at ({x}, {y})")
        self._run_cmd(["adb", "-s", self.device_id, "shell", "input", "swipe", str(x), str(y), str(x), str(y), "100"])
        time.sleep(0.5)  # Default wait after click

    def swipe(self, x1, y1, x2, y2, duration_ms=500):
        """Send a swipe event."""
        print(f"Swiping from ({x1}, {y1}) to ({x2}, {y2})")
        self._run_cmd(["adb", "-s", self.device_id, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)])
        time.sleep(0.5)

    def get_screenshot(self):
        """Pulls a screenshot directly into a numpy array for OpenCV."""
        self._run_cmd(["adb", "-s", self.device_id, "shell", "screencap", "-p", "/sdcard/temp.png"])
        self._run_cmd(["adb", "-s", self.device_id, "pull", "/sdcard/temp.png", "temp.png"])
        img = cv2.imread("temp.png")
        if img is None:
            print("Failed to load screenshot.")
        return img
