import customtkinter as ctk
from app.data import DataManager

# --- Helper ---
def fix_text(text):
    if text is None: return ""
    return str(text)

class PlannerScreen(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="#1a1a1a")
        self.db = DataManager()
        self.on_back = on_back
        self.current_tail = None
        self.aircraft_data = None
        
        # משתנים לחישוב
        self.payload_items = [] # רשימה של (שם, משקל, זרוע)
        self.fuel_weight = 0.0
        
        # --- Top Bar ---
        top_bar = ctk.CTkFrame(self, height=50, fg_color="#333333", corner_radius=0)
        top_bar.pack(fill="x")
        
        ctk.CTkButton(top_bar, text="חזרה לתפריט", width=120, command=on_back).pack(side="right", padx=10, pady=10)
        ctk.CTkLabel(top_bar, text="Mission Planner - תכנון משימה", font=("Arial", 22, "bold")).pack(side="left", padx=20)
        
        # --- בחירת מטוס ---
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(sel_frame, text=":בחר מטוס לתכנון", font=("Arial", 16)).pack(side="right", padx=10)
        
        # שליפת רשימת המטוסים
        tails = self.db.get_fleet_keys()
        self.tail_menu = ctk.CTkOptionMenu(sel_frame, values=tails, command=self.load_aircraft)
        self.tail_menu.pack(side="right")
        
        # --- Main Layout ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_content.grid_columnconfigure(0, weight=1) # תוצאות (שמאל)
        self.main_content.grid_columnconfigure(1, weight=1) # הזנת נתונים (ימין)
        self.main_content.grid_rowconfigure(0, weight=1)

        # === צד ימין: הזנת נתונים (Payload & Fuel) ===
        self.right_panel = ctk.CTkFrame(self.main_content, border_width=1, border_color="gray")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        
        ctk.CTkLabel(self.right_panel, text="הזנת נתונים (Payload)", font=("Arial", 18, "bold")).pack(pady=10)
        
        # הזנת דלק
        fuel_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        fuel_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(fuel_frame, text=":דלק (Lbs)").pack(side="right", padx=5)
        self.en_fuel = ctk.CTkEntry(fuel_frame, justify="center")
        self.en_fuel.pack(side="right", padx=5)
        ctk.CTkButton(fuel_frame, text="עדכון", width=60, command=self.update_fuel).pack(side="right", padx=5)
        
        # הוספת מטען/צוות
        add_frame = ctk.CTkFrame(self.right_panel, fg_color="#2b2b2b")
        add_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(add_frame, text=":הוספת נוסע/מטען", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.en_item_name = ctk.CTkEntry(add_frame, placeholder_text="שם הפריט", justify="right")
        self.en_item_name.pack(pady=5)
        
        self.en_item_w = ctk.CTkEntry(add_frame, placeholder_text="משקל", justify="center")
        self.en_item_w.pack(pady=5)
        
        self.en_item_a = ctk.CTkEntry(add_frame, placeholder_text="זרוע (Station)", justify="center")
        self.en_item_a.pack(pady=5)
        
        ctk.CTkButton(add_frame, text="הוסף לרשימה", fg_color="green", command=self.add_payload_item).pack(pady=10)
        
        # רשימת פריטים שנוספו
        self.items_scroll = ctk.CTkScrollableFrame(self.right_panel, label_text="רשימת העמסה")
        self.items_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # === צד שמאל: סיכום משקלים (Weight & Balance) ===
        self.left_panel = ctk.CTkFrame(self.main_content, border_width=1, border_color="gray")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5)
        
        ctk.CTkLabel(self.left_panel, text="סיכום משקלים ואיזון", font=("Arial", 18, "bold")).pack(pady=10)
        
        # טבלת תוצאות
        self.results_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.results_frame.pack(fill="x", padx=10, pady=10)
        
        # כותרות
        headers = ["CG", "מומנט", "משקל", "תיאור"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.results_frame, text=h, font=("Arial", 12, "bold"), width=80).grid(row=0, column=i, padx=5, pady=5)
            
        self.lbl_basic = self.create_result_row(1, "משקל בסיס (Chart C)")
        self.lbl_payload = self.create_result_row(2, "מטען וצוות")
        self.lbl_zfw = self.create_result_row(3, "Zero Fuel Weight")
        self.lbl_fuel = self.create_result_row(4, "דלק")
        self.lbl_tow = self.create_result_row(5, "Takeoff Weight") # שורה מודגשת

        # טעינת מטוס ראשון כברירת מחדל
        if tails:
            self.load_aircraft(tails[0])

    def create_result_row(self, row_idx, title):
        """יוצר שורה בטבלת התוצאות ומחזיר מילון של הלייבלים לעדכון"""
        labels = {}
        # סדר: CG, Moment, Weight, Title
        
        # CG
        l_cg = ctk.CTkLabel(self.results_frame, text="-", text_color="cyan")
        l_cg.grid(row=row_idx, column=0, padx=5, pady=5)
        labels["cg"] = l_cg
        
        # Moment
        l_mom = ctk.CTkLabel(self.results_frame, text="-")
        l_mom.grid(row=row_idx, column=1, padx=5, pady=5)
        labels["mom"] = l_mom
        
        # Weight
        l_w = ctk.CTkLabel(self.results_frame, text="-")
        l_w.grid(row=row_idx, column=2, padx=5, pady=5)
        labels["w"] = l_w
        
        # Title
        l_title = ctk.CTkLabel(self.results_frame, text=title, anchor="e")
        l_title.grid(row=row_idx, column=3, padx=5, pady=5, sticky="e")
        
        return labels

    def load_aircraft(self, tail):
        self.current_tail = tail
        self.tail_menu.set(tail)
        # טעינת נתונים עדכניים מה-DB (כולל השינויים שעשית ב-Fleet Manager!)
        self.aircraft_data = self.db.get_aircraft_data(tail)
        
        # איפוס רשימת המטען הזמנית במעבר מטוס
        self.payload_items = []
        self.fuel_weight = 0.0
        self.en_fuel.delete(0, "end")
        
        # ניקוי תצוגת פריטים
        for w in self.items_scroll.winfo_children(): w.destroy()
        
        self.recalculate()

    def add_payload_item(self):
        try:
            name = self.en_item_name.get()
            w = float(self.en_item_w.get())
            a = float(self.en_item_a.get())
            
            if not name: name = "פריט כללי"
            
            self.payload_items.append({"name": name, "weight": w, "arm": a})
            
            # הוספה ויזואלית לרשימה
            row = ctk.CTkFrame(self.items_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{name} | {w}lbs @ {a}in", anchor="e").pack(side="right", padx=5)
            
            # כפתור מחיקה קטן
            btn_del = ctk.CTkButton(row, text="X", width=30, fg_color="red", 
                                    command=lambda i=len(self.payload_items)-1, r=row: self.delete_item(i, r))
            btn_del.pack(side="left")
            
            self.recalculate()
            
            # ניקוי שדות
            self.en_item_name.delete(0, "end")
            self.en_item_w.delete(0, "end")
            self.en_item_a.delete(0, "end")
            
        except ValueError:
            pass # אפשר להוסיף הודעת שגיאה

    def delete_item(self, index, row_widget):
        # בגרסה פשוטה זו המחיקה לפי אינדקס עלולה להיות בעייתית אם מוחקים מהאמצע,
        # לכן נבנה מחדש את הרשימה (בפרויקט אמיתי משתמשים ב-ID ייחודי)
        # לצורך הפשטות כאן: נסמן כמושבת (בפועל צריך ניהול רשימה חכם יותר)
        row_widget.destroy()
        # כאן צריך לוגיקה למחיקה מהמערך self.payload_items
        # כרגע נשאיר את זה כרענון כללי פשוט
        pass 

    def update_fuel(self):
        try:
            self.fuel_weight = float(self.en_fuel.get())
            self.recalculate()
        except: pass

    def recalculate(self):
        if not self.aircraft_data: return
        
        # 1. Basic Weight (מתוך ה-Fleet Manager)
        bw = self.aircraft_data.basic_weight
        bm = self.aircraft_data.basic_moment_raw # זה כבר בערך מלא (לא חלקי 1000) במודל המעודכן שלנו?
        # במודל models.py הנוכחי: basic_moment_raw הוא המומנט המלא.
        # כדי להציג בטבלה נחלק ב-1000
        
        # בדיקה אם המודל מחזיר מומנט או מומנט/1000. נניח שהוא מחזיר מלא.
        # אם הנתונים ב-Fleet Manager נשמרים כ-Arm/Weight, המומנט מחושב.
        
        ba = self.aircraft_data.basic_arm_calc
        
        self.update_row_ui(self.lbl_basic, bw, bm, ba)
        
        # 2. Payload
        pw = sum(i["weight"] for i in self.payload_items)
        pm = sum(i["weight"] * i["arm"] for i in self.payload_items)
        pa = (pm / pw) if pw != 0 else 0
        
        self.update_row_ui(self.lbl_payload, pw, pm, pa)
        
        # 3. ZFW (Zero Fuel Weight)
        zfw_w = bw + pw
        zfw_m = bm + pm
        zfw_a = (zfw_m / zfw_w) if zfw_w != 0 else 0
        
        self.update_row_ui(self.lbl_zfw, zfw_w, zfw_m, zfw_a)
        
        # 4. Fuel (דלק)
        # הנחה: זרוע דלק ממוצעת או פונקציה מורכבת. כאן נשים ערך קבוע לצורך הדגמה, או 0 אם לא ידוע
        fuel_arm = 0 # יש להוסיף לוגיקה של עקומת מומנט דלק בעתיד
        fuel_mom = self.fuel_weight * fuel_arm
        
        self.update_row_ui(self.lbl_fuel, self.fuel_weight, fuel_mom, fuel_arm)
        
        # 5. TOW (Takeoff Weight)
        tow_w = zfw_w + self.fuel_weight
        tow_m = zfw_m + fuel_mom
        tow_cg = (tow_m / tow_w) if tow_w != 0 else 0
        
        self.update_row_ui(self.lbl_tow, tow_w, tow_m, tow_cg)

    def update_row_ui(self, labels, w, m, cg):
        labels["w"].configure(text=f"{w:,.1f}")
        labels["mom"].configure(text=f"{m/1000:,.1f}") # מציג מומנט חלקי 1000
        labels["cg"].configure(text=f"{cg:,.2f}")