import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
from app import config

class AircraftDiagram(ctk.CTkFrame):
    def __init__(self, parent, mission_manager, selection_callback, update_callback):
        super().__init__(parent, fg_color="#333333", corner_radius=0)
        self.mgr = mission_manager
        self.on_select = selection_callback
        self.update_callback = update_callback
        self.show_stations = True
        self.show_compartments = True

        # --- Checkboxes (Top Left) ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.place(x=10, y=10)
        
        self.var_st = ctk.BooleanVar(value=True)
        self.var_comp = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(self.controls_frame, text="Comp", variable=self.var_comp, width=60, 
                        font=("Arial", 11, "bold"), text_color="white", command=self.draw).pack(side="left", padx=5)
        ctk.CTkCheckBox(self.controls_frame, text="Stations", variable=self.var_st, width=60, 
                        font=("Arial", 11, "bold"), text_color="white", command=self.draw).pack(side="left", padx=5)

        # --- Canvas ---
        self.canvas = tk.Canvas(self, bg="#404040", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Events
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Key-Delete>", self.on_delete_key)
        self.canvas.bind("<Motion>", self.on_hover)
        
        self.img_original = None
        self.tk_img = None
        self.load_background_image()
        
        # Drag State
        self.drag_item = None
        self.selected_item = None
        self.drag_mode = None
        self.start_x = 0
        self.start_y = 0
        self.orig_ls = 0
        self.orig_y_offset = 0
        self.orig_len = 0
        self.orig_width = 0

    def load_background_image(self):
        path = "assets/plane_bg.png"
        if os.path.exists(path):
            try: self.img_original = Image.open(path)
            except: pass

    def draw(self):
        self.show_stations = self.var_st.get()
        self.show_compartments = self.var_comp.get()

        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 50: return

        # --- כיול ---
        Y_AXIS_SCALE = 2.2 
        REAL_FLOOR_WIDTH_INCHES = 119  # רוחב הרצפה המקסימלי
        
        total_ls_span = config.LS_END - config.LS_START
        margin_x = 20
        scale = (w - (margin_x * 2)) / total_ls_span
        
        base_ref = 120 
        visual_floor_px = base_ref * scale * Y_AXIS_SCALE
        
        mid_y = h / 2
        floor_top_y = mid_y - visual_floor_px/2
        floor_bot_y = mid_y + visual_floor_px/2

        # 1. Background Image
        if self.img_original:
            img_w = int(total_ls_span * scale)
            ratio = self.img_original.height / self.img_original.width
            img_h = int(img_w * ratio)
            resized = self.img_original.resize((img_w, img_h), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(resized)
            self.canvas.create_image(margin_x + img_w/2, mid_y, image=self.tk_img)

        # 2. Compartments (Top)
        if self.show_compartments:
            # קו ייחוס רחוק מהמטוס (35px)
            text_y_comp = floor_top_y - 35 
            line_bottom = floor_top_y      
            
            for comp_name, start_ls, end_ls in config.COMPARTMENT_DEFS:
                x_start = margin_x + (start_ls - config.LS_START) * scale
                x_end = margin_x + (end_ls - config.LS_START) * scale
                x_center = (x_start + x_end) / 2
                
                # קווים לבנים אנכיים
                self.canvas.create_line(x_start, text_y_comp, x_start, line_bottom, fill="white", width=1)
                self.canvas.create_line(x_end, text_y_comp, x_end, line_bottom, fill="white", width=1)
                
                # מספרים (למעלה, רחוק מהאות)
                self.canvas.create_text(x_start, text_y_comp - 8, text=str(start_ls), fill="white", font=("Arial", 9, "bold"))
                self.canvas.create_text(x_end, text_y_comp - 8, text=str(end_ls), fill="white", font=("Arial", 9, "bold"))
                
                # אותיות (למטה, קרוב למטוס - כדי למנוע חפיפה עם המספרים)
                # +25 מוריד את האות לכיוון המטוס
                self.canvas.create_text(x_center, text_y_comp + 25, text=comp_name, fill="cyan", font=("Arial", 14, "bold"))

        # 3. Stations (Bottom)
        if self.show_stations:
            text_y_st = floor_bot_y + 35
            line_top = floor_bot_y
            
            for ls in config.LOAD_STATIONS:
                x = margin_x + (ls - config.LS_START) * scale
                self.canvas.create_line(x, text_y_st - 12, x, line_top, fill="white")
                self.canvas.create_text(x, text_y_st, text=str(ls), fill="white", font=("Arial", 9, "bold"), angle=0)

        # 4. Cargo Items
        for i, item in enumerate(self.mgr.cargo_list):
            cx = margin_x + (item.ls - config.LS_START) * scale
            l_px = item.length * scale
            
            # חישוב רוחב
            w_px = (item.width / REAL_FLOOR_WIDTH_INCHES) * visual_floor_px
            px_per_inch_y = visual_floor_px / REAL_FLOOR_WIDTH_INCHES
            y_offset_px = item.y_offset * px_per_inch_y
            y = mid_y + y_offset_px

            x1, x2 = cx - l_px/2, cx + l_px/2
            y1, y2 = y - w_px/2, y + w_px/2
            
            col = config.COLORS.get(item.item_type, "gray")
            outline = "black"; line_w = 1
            if self.selected_item == item: outline = "white"; line_w = 2
            tag = f"idx_{i}"
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline=outline, width=line_w, tags=("item", tag))
            
            if l_px > 15:
                # טקסט על המטען נשאר שחור לקונטרסט על הצבעים הבהירים
                txt = f"{item.name}\n{int(item.weight)}"
                if l_px > 50: txt += f"\nLoc: {int(item.ls)}"
                self.canvas.create_text(cx, y, text=txt, fill="black", font=("Arial", 8, "bold"), justify="center", tags=("item", tag))
        
        # 5. Crew Markers
        for crew in self.mgr.crew_list:
            if crew.type in ["Seat", "Sofa"]: continue
            cx = margin_x + (crew.ls - config.LS_START) * scale
            cy = mid_y 
            self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="orange", outline="black")
            self.canvas.create_text(cx, cy, text="LM", font=("Arial",7,"bold"))
            
        self.controls_frame.lift()

    def on_click(self, e):
        self.canvas.focus_set()
        items = self.canvas.find_withtag("current")
        if not items: 
            self.selected_item = None
            self.on_select(None)
            self.draw()
            return
        
        tags = self.canvas.gettags(items[0])
        idx = -1
        for t in tags:
            if t.startswith("idx_"): idx = int(t.split("_")[1]); break
        
        if idx != -1:
            self.selected_item = self.mgr.cargo_list[idx]
            self.drag_item = self.selected_item
            self.on_select(self.selected_item)
            
            self.start_x, self.start_y = e.x, e.y
            self.orig_ls = self.drag_item.ls
            self.orig_y_offset = self.drag_item.y_offset
            self.orig_len = self.drag_item.length
            self.orig_width = self.drag_item.width
            
            bbox = self.canvas.coords(items[0])
            is_gen = (self.drag_item.item_type == "Gen")
            
            # זיהוי אזורי גרירה
            if abs(e.x - bbox[2]) < 10: 
                self.drag_mode = "resize_len"
            elif is_gen and (abs(e.y - bbox[1]) < 10 or abs(e.y - bbox[3]) < 10): 
                self.drag_mode = "resize_wid"
            else: 
                self.drag_mode = "move"

    def on_drag(self, e):
        if not self.drag_item: return
        w = self.canvas.winfo_width()
        total_ls_span = config.LS_END - config.LS_START
        margin_x = 20
        scale_x = (w - (margin_x * 2)) / total_ls_span
        
        REAL_FLOOR_WIDTH_INCHES = 119
        base_ref = 120
        Y_AXIS_SCALE = 2.2
        visual_floor_px = base_ref * scale_x * Y_AXIS_SCALE
        px_per_inch_y = visual_floor_px / REAL_FLOOR_WIDTH_INCHES
        
        if self.drag_mode == "move":
            # X Axis
            dx_px = e.x - self.start_x
            dx_inch = dx_px / scale_x
            self.drag_item.ls = self.orig_ls + dx_inch
            
            # Y Axis
            dy_px = e.y - self.start_y
            dy_inch = dy_px / px_per_inch_y
            new_y_offset = self.orig_y_offset + dy_inch
            
            # בדיקת גבולות (חצי מ-119 זה 59.5 לכל צד)
            limit = 59.5 - (self.drag_item.width / 2)
            if abs(new_y_offset) <= limit:
                self.drag_item.y_offset = new_y_offset
            
        elif self.drag_mode == "resize_len":
            dx_px = e.x - self.start_x
            dx_inch = dx_px / scale_x
            self.drag_item.length = max(12, self.orig_len + dx_inch)

        elif self.drag_mode == "resize_wid":
            # חישוב רוחב חדש ע"י מרחק מהמרכז
            mid_y = self.canvas.winfo_height() / 2
            item_y_center_px = mid_y + (self.drag_item.y_offset * px_per_inch_y)
            dist_from_center = abs(e.y - item_y_center_px)
            new_width = (dist_from_center * 2) / px_per_inch_y
            self.drag_item.width = min(new_width, 119) # מגבלת רוחב

        # Live Update
        if self.on_select:
            self.on_select(self.drag_item)
            
        self.update_callback()
        self.draw()

    def on_release(self, e): 
        self.drag_item = None
        self.draw()

    def on_delete_key(self, event):
        if self.selected_item: 
            self.mgr.remove_cargo(self.selected_item)
            self.selected_item = None
            self.on_select(None)
            self.draw()

    def on_hover(self, e):
        items = self.canvas.find_withtag("current")
        if items and "item" in self.canvas.gettags(items[0]):
            bbox = self.canvas.coords(items[0])
            tags = self.canvas.gettags(items[0])
            idx = int(tags[1].split("_")[1])
            item = self.mgr.cargo_list[idx]
            
            # שינוי סמן
            if abs(e.x - bbox[2]) < 10: 
                self.canvas.config(cursor="sb_h_double_arrow")
            elif item.item_type == "Gen" and (abs(e.y - bbox[1]) < 10 or abs(e.y - bbox[3]) < 10):
                self.canvas.config(cursor="sb_v_double_arrow")
            else:
                self.canvas.config(cursor="hand2")
        else: 
            self.canvas.config(cursor="")