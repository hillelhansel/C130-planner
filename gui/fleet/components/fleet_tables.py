import customtkinter as ctk

class ConfigTable(ctk.CTkFrame):
    def __init__(self, parent, on_change_callback, on_delete_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change_callback
        self.on_delete = on_delete_callback
        
        # שמירת הווידג'טים לשימוש חוזר כדי למנוע איטיות
        self.rows_cache = [] 

        # Header
        headers_frame = ctk.CTkFrame(self, fg_color="#444", height=35, corner_radius=10)
        headers_frame.pack(fill="x", pady=(0, 2))
        
        # Columns
        cols = [
            ("Item Name", 220), ("Unit Wt", 70), ("Std", 50), ("Actual", 100), 
            ("Rem", 50), ("Rem Wt", 80), ("Arm", 60), ("Moment", 70), ("", 30)
        ]
        
        for txt, w in cols:
            ctk.CTkLabel(headers_frame, text=txt, width=w, font=("Arial", 14, "bold"), 
                         text_color="white", anchor="center").pack(side="left", padx=1)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#222")
        self.scroll.pack(fill="both", expand=True, pady=2)

    def load_data(self, config_items):
        """
        פונקציה חכמה: בונה שורות רק אם חסר, אחרת רק מעדכנת.
        זה מונע את ה-Lag במעבר בין מטוסים.
        """
        # 1. התאמת מספר השורות הגרפיות למספר הפריטים בנתונים
        current_rows = len(self.rows_cache)
        needed_rows = len(config_items)

        # אם יש יותר מדי שורות (למשל מחקנו פריט), נעלים את המיותרות
        if current_rows > needed_rows:
            for i in range(needed_rows, current_rows):
                self.rows_cache[i]['frame'].pack_forget()
        
        # אם חסרות שורות, ניצור חדשות
        if needed_rows > current_rows:
            for i in range(current_rows, needed_rows):
                self._create_new_row_widget(i)

        # 2. עדכון הנתונים בכל השורות (Binding)
        for i, item in enumerate(config_items):
            self._bind_row_data(i, item)
            # וודא שהשורה מוצגת (למקרה שהוסתרה קודם)
            self.rows_cache[i]['frame'].pack(fill="x", pady=2)

    def _create_new_row_widget(self, index):
        font_row = ("Arial", 12)
        row = ctk.CTkFrame(self.scroll, fg_color="transparent", height=30)
        
        # יצירת הווידג'טים ושמירת רפרנס אליהם
        widgets = {'frame': row}
        
        # Name
        widgets['name'] = ctk.CTkLabel(row, text="", width=220, font=font_row, anchor="w")
        widgets['name'].pack(side="left", padx=1)
        
        # Unit Wt
        widgets['unit_wt'] = ctk.CTkLabel(row, text="", width=70, font=font_row)
        widgets['unit_wt'].pack(side="left", padx=1)
        
        # Std
        widgets['std'] = ctk.CTkLabel(row, text="", width=50, font=font_row)
        widgets['std'].pack(side="left", padx=1)
        
        # Actual (+/-)
        act_frame = ctk.CTkFrame(row, fg_color="transparent", width=100)
        act_frame.pack(side="left", padx=1)
        
        # אנחנו משתמשים ב-lambda עם משתנה שמועבר בפונקציה נפרדת בעת ה-Bind
        # כאן רק העיצוב
        btn_minus = ctk.CTkButton(act_frame, text="-", width=24, height=24, fg_color="#444", hover_color="red", font=("Arial",12,"bold"))
        btn_minus.pack(side="left", padx=2)
        widgets['btn_minus'] = btn_minus
        
        widgets['actual'] = ctk.CTkLabel(act_frame, text="", width=24, font=("Arial", 13, "bold"))
        widgets['actual'].pack(side="left", padx=2)
        
        btn_plus = ctk.CTkButton(act_frame, text="+", width=24, height=24, fg_color="#444", hover_color="green", font=("Arial",12,"bold"))
        btn_plus.pack(side="left", padx=2)
        widgets['btn_plus'] = btn_plus
        
        # Calc Fields
        widgets['rem'] = ctk.CTkLabel(row, text="", width=50, font=font_row, text_color="gray")
        widgets['rem'].pack(side="left", padx=1)
        
        widgets['rem_wt'] = ctk.CTkLabel(row, text="", width=80, font=font_row, text_color="gray")
        widgets['rem_wt'].pack(side="left", padx=1)
        
        widgets['arm'] = ctk.CTkLabel(row, text="", width=60, font=font_row)
        widgets['arm'].pack(side="left", padx=1)
        
        widgets['mom'] = ctk.CTkLabel(row, text="", width=70, font=font_row, text_color="gray")
        widgets['mom'].pack(side="left", padx=1)

        # Delete
        btn_del = ctk.CTkButton(row, text="✕", width=30, height=24, fg_color="transparent", text_color="#ff5555", hover_color="#440000", font=("Arial", 12, "bold"))
        btn_del.pack(side="left", padx=5)
        widgets['btn_del'] = btn_del

        self.rows_cache.append(widgets)

    def _bind_row_data(self, index, item):
        # פונקציה מהירה שרק משנה טקסט ופקודות
        w = self.rows_cache[index]
        
        removed = item.full_qty - item.qty_in_plane
        rem_wt = removed * item.weight_per_unit
        rem_mom = (rem_wt * item.ls) / 1000.0
        col = "#ff5555" if removed > 0 else "gray"

        w['name'].configure(text=item.name)
        w['unit_wt'].configure(text=f"{item.weight_per_unit:.0f}")
        w['std'].configure(text=str(item.full_qty))
        w['actual'].configure(text=str(item.qty_in_plane))
        
        w['rem'].configure(text=str(removed), text_color=col)
        w['rem_wt'].configure(text=f"{rem_wt:.1f}", text_color=col)
        w['arm'].configure(text=f"{item.ls:.0f}")
        w['mom'].configure(text=f"{rem_mom:.2f}", text_color=col)

        # עדכון פקודות הכפתורים כך שיצביעו לאינדקס הנוכחי
        # חשוב: יש להגדיר מחדש את הפקודה בכל עדכון כי האינדקסים עלולים להשתנות במחיקה
        w['btn_minus'].configure(command=lambda: self.on_change(index, -1))
        w['btn_plus'].configure(command=lambda: self.on_change(index, 1))
        w['btn_del'].configure(command=lambda: self.on_delete(index))


class UpdatesTable(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        h = ctk.CTkFrame(self, fg_color="#444", height=35, corner_radius=10)
        h.pack(fill="x", pady=(0, 2))
        
        headers = ["Date", "Updater", "Description", "Weight", "Arm", "Moment"]
        widths = [100, 100, 220, 70, 70, 70]
        
        for txt, w in zip(headers, widths):
            ctk.CTkLabel(h, text=txt, width=w, font=("Arial", 14, "bold"), text_color="white", anchor="center").pack(side="left", padx=1)
            
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.scroll.pack(fill="both", expand=True)

    def refresh(self, aircraft_data):
        # טבלת העדכונים קצרה בדרך כלל, אז אפשר לנקות ולבנות מחדש
        # אבל גם כאן עדיף לא להגזים. נשאיר פשוט כי יש מעט שורות יחסית.
        for w in self.scroll.winfo_children(): w.destroy()
        
        row_font = ("Arial", 12)
        widths = [100, 100, 220, 70, 70, 70]
        
        def add_row(vals, colors=None):
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", pady=2, anchor="center")
            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(anchor="center")
            for i, v in enumerate(vals):
                col = colors[i] if colors else "white"
                ctk.CTkLabel(inner, text=v, width=widths[i], font=row_font, text_color=col, anchor="center").pack(side="left", padx=1)

        # Weighing
        add_row(
            ["-", "Manuf./Weigh", "Basic Weighing", f"{aircraft_data.weighing_weight:,.1f}", f"{aircraft_data.weighing_arm:.1f}", f"{aircraft_data.weighing_moment:,.1f}"],
            colors=["gray"]*6
        )

        # Updates
        for u in aircraft_data.update_items:
            c = "green" if u.weight_change >= 0 else "red"
            add_row(
                [u.date, u.adjuster, u.description, f"{u.weight_change:+.1f}", f"{u.arm_change:.1f}", f"{u.moment_change:.2f}"],
                colors=["white", "white", "white", c, "white", "white"]
            )