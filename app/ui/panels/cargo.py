import customtkinter as ctk
from .base import BaseSection
from app import config
from app.models import CargoItem
from app.data import DataManager  # חיבור למסד הנתונים

class CargoSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        self.db = DataManager() # טעינת הנתונים
        self.section = BaseSection(parent, "4. ADD CARGO")
        
        # --- אזור הקטלוג (Catalog) ---
        cat_frame = ctk.CTkFrame(self.section.content, fg_color="transparent")
        cat_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(cat_frame, text="From Catalog:", font=("Arial", 11, "bold"), text_color="orange").pack(side="left")
        
        self.cat_var = ctk.StringVar(value="Select Item")
        # שליפת הפריטים מה-Database במקום מקובץ קונפיג סטטי
        cat_opts = list(self.db.get_catalog().keys())
        
        self.cb_catalog = ctk.CTkComboBox(cat_frame, values=cat_opts, variable=self.cat_var, width=120, command=self.load_from_catalog)
        self.cb_catalog.pack(side="left", padx=5)
        
        # כפתור רענון קטן (למקרה שעדכנו את הקטלוג במסך אחר)
        ctk.CTkButton(cat_frame, text="⟳", width=30, command=self.refresh_catalog).pack(side="left", padx=2)

        # --- לשוניות (Tabs) ---
        tabs = ctk.CTkTabview(self.section.content, height=320)
        tabs.pack(fill="x")
        
        self.mk_tab(tabs.add("PAX"), "Pax", "Pax", 20, 20, "Pax", has_pax=True, allow_comp=True)
        self.mk_tab(tabs.add("PALLET"), "Pallet", "Log Pallet", 90, 108, "Pallet", allow_comp=False)
        self.mk_tab(tabs.add("HEAVY"), "Metric", "Metric", 0, 108, "Metric", is_metric=True, allow_comp=False)
        self.mk_tab(tabs.add("CDS"), "Drop", "CDS", 48, 48, "Drop", is_cds=True, allow_comp=False)
        self.mk_tab(tabs.add("GEN"), "Gen", "Gen", 48, 80, "Gen", is_gen=True, allow_comp=True)

    def refresh_catalog(self):
        """רענון רשימת הקטלוג מה-DB"""
        self.db = DataManager() # טעינה מחדש
        cat_opts = list(self.db.get_catalog().keys())
        self.cb_catalog.configure(values=cat_opts)

    def load_from_catalog(self, choice):
        """טעינת פריט מהקטלוג והוספתו למשימה"""
        data = self.db.get_catalog().get(choice)
        if data:
            # הוספה מהירה למרכז (דיפולט LS 500)
            item = CargoItem(choice, data['weight'], 500, data['length'], data['width'], data['type'], "Center")
            self.mgr.add_cargo(item)
            self.cat_var.set("Select Item")

    def mk_tab(self, t, type_code, dname, dl, dw, dtype, has_pax=False, is_metric=False, is_cds=False, is_gen=False, allow_comp=False):
        # שם המטען
        en = ctk.CTkEntry(t, placeholder_text="Name"); en.insert(0, dname); en.pack(pady=2)
        
        # משתנים לשמירת נתוני התא
        self.comp_var = ctk.StringVar(value="")
        self.comp_count = None

        # --- לוגיקת בחירת תא (רק ל-GEN ו-PAX) ---
        if allow_comp:
            comp_frame = ctk.CTkFrame(t, fg_color="transparent"); comp_frame.pack(pady=2)
            ctk.CTkLabel(comp_frame, text="Comp:").pack(side="left")
            comp_opts = [c[0] for c in config.COMPARTMENT_DEFS]
            cb_comp = ctk.CTkComboBox(comp_frame, values=[""] + comp_opts, width=60, variable=self.comp_var)
            cb_comp.pack(side="left", padx=5)

            if is_gen:
                ctk.CTkLabel(comp_frame, text="Count:").pack(side="left", padx=2)
                self.comp_count = ctk.CTkEntry(comp_frame, width=30); self.comp_count.insert(0, "1"); self.comp_count.pack(side="left")

        # --- אופציות ייחודיות ---
        if has_pax:
            ctk.CTkComboBox(t, values=["Regular (175)", "Para (220)", "Combat (250)"], 
                            command=lambda v: [ew.delete(0,"end"), ew.insert(0, v.split("(")[1][:-1])]).pack(pady=2)
        if is_metric: 
            cmb_m = ctk.CTkComboBox(t, values=[f"{i} ft" for i in range(8,33,4)]); cmb_m.pack(pady=2)
        if is_cds: 
            cmb_ct = ctk.CTkComboBox(t, values=["CDS 48", "CDS 52", "BSA"]); cmb_ct.pack(pady=2)
            cmb_cs = ctk.CTkComboBox(t, values=["Center", "Right Stick", "Left Stick"]); cmb_cs.pack(pady=2)
        
        # משקל
        ew = ctk.CTkEntry(t, placeholder_text="Weight"); ew.pack(pady=2)
        
        # מיקום (LS/CG)
        pos_frame = ctk.CTkFrame(t, fg_color="transparent"); pos_frame.pack(pady=2)
        els = ctk.CTkEntry(pos_frame, width=60, placeholder_text="Center LS"); els.pack(side="left", padx=2)
        ecg = ctk.CTkEntry(pos_frame, width=60, placeholder_text="CG LS"); ecg.pack(side="left", padx=2)
        
        # עדכון אוטומטי בבחירת תא
        if allow_comp:
            cb_comp.configure(command=lambda x: self.on_comp_select(x, els, ecg))
        
        # סנכרון CG עם LS בהקלדה
        els.bind("<KeyRelease>", lambda e: ecg.delete(0, "end") or ecg.insert(0, els.get()))

        # מידות ידניות (ל-GEN בלבד)
        if is_gen:
            gf = ctk.CTkFrame(t, fg_color="transparent"); gf.pack(pady=2)
            el = ctk.CTkEntry(gf, width=50); el.insert(0, str(dl)); el.pack(side="left")
            ewi = ctk.CTkEntry(gf, width=50); ewi.insert(0, str(dw)); ewi.pack(side="left")

        # --- פונקציית ההוספה ---
        def add():
            try:
                # ערכי ברירת מחדל
                l, w, s = dl, dw, "Center"
                y_off = 0.0
                
                # בדיקה אם נבחר תא (רק ב-Gen/Pax)
                is_comp_mode = False
                if allow_comp and self.comp_var.get() != "":
                    is_comp_mode = True
                    
                    # חישוב אורך לפי מספר תאים (למשל מ-C ל-D)
                    if is_gen:
                        try:
                            count = int(self.comp_count.get())
                            start_comp = self.comp_var.get()
                            # מציאת האינדקס של התא ברשימה
                            idx = next((i for i, item in enumerate(config.COMPARTMENT_DEFS) if item[0] == start_comp), -1)
                            
                            if idx != -1 and idx + count <= len(config.COMPARTMENT_DEFS):
                                start_ls_val = config.COMPARTMENT_DEFS[idx][1]
                                end_ls_val = config.COMPARTMENT_DEFS[idx+count-1][2]
                                l = end_ls_val - start_ls_val
                        except: pass
                    
                    # הגדרות ויזואליות למטען בתוך תא (צר וגבוה)
                    w = 20.0  # רוחב צר
                    y_off = -50.0 # הזחה למעלה בדיאגרמה

                # אם לא במצב תא - לוקחים מידות מהשדות הידניים
                elif is_gen:
                    l, w = float(el.get()), float(ewi.get())

                # התאמות לסוגים מיוחדים
                if is_metric: l = int(cmb_m.get().split()[0])*12
                if is_cds:
                    tp = cmb_ct.get(); en.delete(0,"end"); en.insert(0, tp)
                    if "52" in tp: l,w = 52,52
                    if "BSA" in tp: l,w = 48,108
                    else: s = cmb_cs.get()
                
                # יצירת האובייקט
                item = CargoItem(en.get(), float(ew.get()), float(ecg.get()), l, w, dtype, s)
                item.ls = float(els.get()) # מיקום פיזי
                
                if is_comp_mode:
                    item.y_offset = y_off # עדכון Y ידני רק אם זה תא
                
                self.mgr.add_cargo(item)
            except: pass
            
        ctk.CTkButton(t, text="ADD", command=add).pack(pady=5)

    def on_comp_select(self, choice, entry_ls, entry_cg):
        """עדכון השדות האוטומטי בבחירת תא"""
        for c, s, e in config.COMPARTMENT_DEFS:
            if c == choice:
                center = (s + e) / 2
                entry_ls.delete(0, "end"); entry_ls.insert(0, str(int(center)))
                entry_cg.delete(0, "end"); entry_cg.insert(0, str(int(center)))
                break