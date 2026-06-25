import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os
import subprocess

BBOX_FILE = "bounding_boxes.json"

class BBoxMapper:
    def __init__(self, root):
        self.root = root
        self.root.title("FC Mobile - Bounding Box Mapper")
        
        self.bboxes = self.load_bboxes()
        
        # We scale the image down so it fits on your computer monitor
        # The coordinates will automatically be scaled back to 100% when saved!
        self.scale_factor = 0.8
        
        # UI Setup
        self.setup_ui()
        
        # State variables
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.image = None
        self.photo = None
        
        self.refresh_screenshot()
        
    def load_bboxes(self):
        if os.path.exists(BBOX_FILE):
            with open(BBOX_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_bboxes(self):
        with open(BBOX_FILE, 'w') as f:
            json.dump(self.bboxes, f, indent=4)

    def setup_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        btn_refresh = tk.Button(toolbar, text="📸 Refresh Screenshot", command=self.refresh_screenshot, bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        btn_clear = tk.Button(toolbar, text="🗑️ Clear All Boxes", command=self.clear_all, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Sidebar for current bboxes
        sidebar = tk.Frame(self.root, width=200, bg="#ecf0f1", padx=10, pady=10)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(sidebar, text="Saved Boxes", bg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.listbox = tk.Listbox(sidebar, font=("Arial", 11))
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.delete_box)
        tk.Label(sidebar, text="(Double-click to delete)", bg="#ecf0f1", font=("Arial", 9, "italic")).pack(pady=5)
        
        self.update_listbox()
        
        # Canvas
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for name in self.bboxes.keys():
            self.listbox.insert(tk.END, name)

    def delete_box(self, event):
        selection = self.listbox.curselection()
        if selection:
            name = self.listbox.get(selection[0])
            if messagebox.askyesno("Delete", f"Are you sure you want to delete the box: '{name}'?"):
                del self.bboxes[name]
                self.save_bboxes()
                self.update_listbox()
                self.draw_all_boxes()

    def clear_all(self):
        if messagebox.askyesno("Clear All", "WARNING: Are you sure you want to delete ALL bounding boxes?"):
            self.bboxes = {}
            self.save_bboxes()
            self.update_listbox()
            self.draw_all_boxes()

    def refresh_screenshot(self):
        print("Pulling live screenshot from device...")
        try:
            # Tell ADB to take a screenshot and pull it to our PC
            subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/mapper_screen.png"], check=True)
            subprocess.run(["adb", "pull", "/sdcard/mapper_screen.png", "mapper_screen.png"], check=True, capture_output=True)
            
            img = Image.open("mapper_screen.png")
            
            # Resize image to fit screen
            new_width = int(img.width * self.scale_factor)
            new_height = int(img.height * self.scale_factor)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.image = img
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=new_width, height=new_height)
            self.draw_all_boxes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get screenshot from device. Make sure emulator is running!\n{e}")

    def draw_all_boxes(self):
        self.canvas.delete("all")
        if self.photo:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
        for name, bbox in self.bboxes.items():
            x1, y1, x2, y2 = bbox
            
            # Scale coordinates down for display
            sx1 = x1 * self.scale_factor
            sy1 = y1 * self.scale_factor
            sx2 = x2 * self.scale_factor
            sy2 = y2 * self.scale_factor
            
            # Draw the box
            self.canvas.create_rectangle(sx1, sy1, sx2, sy2, outline="#00ff00", width=3)
            
            # Draw the label background and text
            self.canvas.create_rectangle(sx1, sy1-20, sx1 + len(name)*8 + 10, sy1, fill="#00ff00", outline="#00ff00")
            self.canvas.create_text(sx1 + 5, sy1-10, text=name, fill="black", anchor=tk.W, font=("Arial", 10, "bold"))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="#3498db", width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.current_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        # Ensure we have proper coordinates (top-left to bottom-right)
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        # Only prompt if they dragged a box bigger than 5 pixels (prevents accidental clicks)
        if x2 - x1 > 5 and y2 - y1 > 5:
            name = simpledialog.askstring("Name this Box", "What data is inside this box? (e.g. 'height', 'player_name'):")
            if name:
                # Scale coordinates up to original game resolution
                orig_x1 = int(x1 / self.scale_factor)
                orig_y1 = int(y1 / self.scale_factor)
                orig_x2 = int(x2 / self.scale_factor)
                orig_y2 = int(y2 / self.scale_factor)
                
                self.bboxes[name] = [orig_x1, orig_y1, orig_x2, orig_y2]
                self.save_bboxes()
                self.update_listbox()
        
        self.draw_all_boxes()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#2c3e50")
    app = BBoxMapper(root)
    root.mainloop()
