import subprocess
import time
import cv2
import numpy as np

class ADBController:
    def __init__(self, device_id="emulator-5554"):
        self.device_id = device_id
        # Ensure device is connected
        subprocess.run(["adb", "devices"], capture_output=True)
        
        # Open persistent ADB shell for lightning-fast inputs (Zero overhead)
        self.shell = subprocess.Popen(
            ["adb", "-s", self.device_id, "shell"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("Production Persistent ADB Shell Initialized.")

    def _run_cmd(self, cmd):
        """Legacy command runner for things that can't use persistent shell."""
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ADB Error: {result.stderr}")
        return result.stdout
        
    def _send_shell(self, cmd_str):
        """Send instant command to persistent shell."""
        if self.shell.stdin:
            self.shell.stdin.write(cmd_str + "\n")
            self.shell.stdin.flush()

    def click(self, x, y):
        """Instant tap using persistent shell."""
        print(f"Clicking at ({x}, {y})")
        self._send_shell(f"input swipe {x} {y} {x} {y} 50")

    def swipe(self, x1, y1, x2, y2, duration_ms=500):
        """Instant swipe using persistent shell."""
        print(f"Swiping from ({x1}, {y1}) to ({x2}, {y2})")
        self._send_shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
        
    def input_text(self, text):
        """Instant text input using persistent shell."""
        self._send_shell(f"input text '{text}'")
        
    def keyevent(self, keycode):
        """Instant keyevent using persistent shell."""
        self._send_shell(f"input keyevent {keycode}")

    def get_screenshot(self):
        """Pulls a screenshot directly into a memory buffer stream (no disk writes = insanely fast)."""
        # We must use a separate subprocess for exec-out because it streams binary
        process = subprocess.Popen(
            ["adb", "-s", self.device_id, "exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        image_bytes, _ = process.communicate()
        
        if not image_bytes:
            print("Failed to capture screen.")
            return None
            
        # Decode memory bytes directly into OpenCV image
        img_array = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
