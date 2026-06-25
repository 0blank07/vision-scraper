import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
from adb_controller import ADBController

class CoordinateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinate Teller for FC Mobile")
        
        # Initialize ADB
        self.adb = ADBController()
        
        # UI Setup
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill=tk.X, pady=10)
        
        self.refresh_btn = tk.Button(self.top_frame, text="Refresh Screenshot", command=self.refresh_screenshot, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.refresh_btn.pack(side=tk.LEFT, padx=15)
        
        self.coord_label = tk.Label(self.top_frame, text="X: 0, Y: 0", font=("Arial", 14, "bold"), fg="blue")
        self.coord_label.pack(side=tk.LEFT, padx=20)
        
        self.info_label = tk.Label(self.top_frame, text="Scaled to fit screen. Click to copy true coordinates.", font=("Arial", 12))
        self.info_label.pack(side=tk.RIGHT, padx=15)
        
        # --- SCALING LOGIC ---
        # 1600x900 is often too big for laptop screens. We scale it down by 0.7
        self.scale_factor = 0.7
        self.canvas_w = int(1600 * self.scale_factor)
        self.canvas_h = int(900 * self.scale_factor)
        
        # Canvas for the resized image
        self.canvas = tk.Canvas(root, width=self.canvas_w, height=self.canvas_h, cursor="crosshair", bg="black")
        self.canvas.pack()
        
        # Bind mouse events
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        
        self.current_image = None
        self.photo = None
        self.marker = None
        
        # Load the initial screenshot immediately
        self.refresh_screenshot()
        
    def refresh_screenshot(self):
        self.refresh_btn.config(text="Loading Screenshot...", state=tk.DISABLED)
        threading.Thread(target=self._get_screenshot_task, daemon=True).start()
        
    def _get_screenshot_task(self):
        img_np = self.adb.get_screenshot()
        if img_np is not None:
            # Convert to RGB
            img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            
            # Resize image to fit screen based on scale factor
            self.current_image = pil_img.resize((self.canvas_w, self.canvas_h), Image.Resampling.LANCZOS)
            
            self.root.after(0, self._update_canvas)
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "Failed to get screenshot."))
        
        self.root.after(0, lambda: self.refresh_btn.config(text="Refresh Screenshot", state=tk.NORMAL))
        
    def _update_canvas(self):
        if self.current_image:
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.marker = None

    def on_mouse_move(self, event):
        # Convert the scaled canvas coordinates back to true 1600x900 coordinates
        true_x = int(event.x / self.scale_factor)
        true_y = int(event.y / self.scale_factor)
        self.coord_label.config(text=f"Live X: {true_x},  Y: {true_y}")
        
    def on_mouse_click(self, event):
        true_x = int(event.x / self.scale_factor)
        true_y = int(event.y / self.scale_factor)
        coord_text = f"{true_x}, {true_y}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(coord_text)
        self.root.update()
        
        self.info_label.config(text=f"Copied TRUE coords: ({coord_text})", fg="green")
        
        if self.marker:
            self.canvas.delete(self.marker)
        r = 6
        self.marker = self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, outline="yellow", width=2, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = CoordinateFinderApp(root)
    root.mainloop()
