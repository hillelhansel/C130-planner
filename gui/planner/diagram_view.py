import customtkinter as ctk
from PIL import Image, ImageTk
import os

class DiagramView(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent")
        self.mgr = manager
        
        # כותרת
        ctk.CTkLabel(self, text="C.G. Envelope Visualization", font=("Arial", 16, "bold")).pack(pady=10)
        
        # קנבס לציור
        self.canvas = ctk.CTkCanvas(self, bg="#222", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.plane_img_ref = None # חובה לשמור רפרנס
        self.load_image()
        
        # האזנה לשינויי גודל
        self.canvas.bind("<Configure>", self.on_resize)

    def load_image(self):
        try:
            # נתיב לקובץ
            img_path = os.path.join("assets", "plane_bg.png")
            if os.path.exists(img_path):
                self.orig_image = Image.open(img_path)
            else:
                self.orig_image = None
                print(f"Error: Image not found at {img_path}")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.orig_image = None

    def on_resize(self, event):
        self.draw()

    def refresh(self):
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 10 or h < 10: return

        # 1. ציור תמונת המטוס
        plane_bounds = None
        
        if self.orig_image:
            # חישוב יחס גובה-רוחב כדי לשמור על פרופורציות
            img_w, img_h = self.orig_image.size
            ratio = min(w / img_w, h / img_h) * 0.9 # תופס 90% מהשטח
            
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            
            resized = self.orig_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.plane_img_ref = ImageTk.PhotoImage(resized)
            
            cx, cy = w / 2, h / 2
            self.canvas.create_image(cx, cy, image=self.plane_img_ref)
            
            # שמירת גבולות המטוס לטובת חישוב מיקום ה-CG
            plane_bounds = {
                'x': cx - new_w/2, 'y': cy - new_h/2,
                'w': new_w, 'h': new_h
            }
        else:
            self.canvas.create_text(w/2, h/2, text="[Plane Image Missing]", fill="gray")
            return

        # 2. ציור קו ה-CG
        res = self.mgr.get_results()
        cg_percent = res.get("CG", 0)
        
        if plane_bounds:
            px = plane_bounds['x']
            py = plane_bounds['y']
            pw = plane_bounds['w']
            ph = plane_bounds['h']
            
            # כיול: נניח שה-MAC מתחיל ב-35% ונגמר ב-65% מאורך המטוס בתמונה
            # (בפועל תצטרך להתאים את המספרים האלה לתמונה הספציפית שלך)
            mac_start_x = px + (pw * 0.35)
            mac_width = pw * 0.30 # אורך ה-MAC בפיקסלים (30% מהמטוס)
            
            # חישוב מיקום ה-X של ה-CG
            # CG הוא באחוזים (למשל 25%), אז נמיר לפיקסלים בתוך ה-MAC
            cg_x = mac_start_x + (cg_percent / 100.0 * mac_width)
            
            # ציור הקו
            self.canvas.create_line(cg_x, py, cg_x, py + ph, fill="cyan", width=3, dash=(4, 2))
            
            # כיתוב
            self.canvas.create_text(cg_x, py - 15, text=f"CG: {cg_percent:.1f}%", fill="cyan", font=("Arial", 12, "bold"))