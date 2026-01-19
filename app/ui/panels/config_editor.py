# app/ui/panels/config_editor.py
import customtkinter as ctk

class ConfigEditorPanel(ctk.CTkFrame):
    def __init__(self, parent, config_list, on_change_callback, is_editable=True):
        super().__init__(parent, fg_color="#2b2b2b")
        self.config_list = config_list
        self.on_change = on_change_callback
        self.is_editable = is_editable

        # Headers
        headers = ctk.CTkFrame(self, fg_color="#444444", height=30)
        headers.pack(fill="x", padx=2, pady=2)
        
        # עמודות בטבלה
        cols = [("Item Name", 140), ("Wt", 40), ("Arm", 40), ("Qty", 70), ("Total", 50)]
        for txt, w in cols:
            ctk.CTkLabel(headers, text=txt, width=w, font=("Arial", 11, "bold")).pack(side="left", padx=1)

        # רשימה נגללת
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)
        
        self.render_items()
        
        # שורת סיכום למטה
        self.footer = ctk.CTkFrame(self, fg_color="#333333", height=35)
        self.footer.pack(fill="x", pady=5)
        self.lbl_total = ctk.CTkLabel(self.footer, text="Total: 0", font=("Arial", 12, "bold"), text_color="cyan")
        self.lbl_total.pack()
        self.update_totals()

    def render_items(self):
        # ניקוי ישן
        for w in self.scroll.winfo_children(): w.destroy()
        
        # מיון: קודם פריטי בסיס (Standard), אחר כך Role
        sorted_list = sorted(self.config_list, key=lambda x: x.category, reverse=True)

        for item in sorted_list:
            # בחירת צבע רקע לפי סוג (ירוק כהה / אדום כהה)
            bg_col = "#2A402A" if item.category == "Standard" else "#402A2A"
            
            row = ctk.CTkFrame(self.scroll, fg_color=bg_col)
            row.pack(fill="x", pady=1)
            
            ctk.CTkLabel(row, text=item.name, width=140, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(int(item.weight)), width=40).pack(side="left")
            ctk.CTkLabel(row, text=str(int(item.ls)), width=40).pack(side="left")
            
            # שליטה בכמות
            qty_frame = ctk.CTkFrame(row, fg_color="transparent", width=70)
            qty_frame.pack(side="left")
            
            btn_minus = ctk.CTkButton(qty_frame, text="-", width=22, height=22, fg_color="#555555",
                                      command=lambda i=item: self.change_qty(i, -1))
            btn_minus.pack(side="left")
            
            lbl_qty = ctk.CTkLabel(qty_frame, text=str(item.qty), width=20, font=("Arial", 12, "bold"))
            lbl_qty.pack(side="left")
            
            btn_plus = ctk.CTkButton(qty_frame, text="+", width=22, height=22, fg_color="#555555",
                                     command=lambda i=item: self.change_qty(i, 1))
            btn_plus.pack(side="left")
            
            # סך משקל לפריט
            lbl_tot = ctk.CTkLabel(row, text=str(int(item.total_weight)), width=50)
            lbl_tot.pack(side="left")
            
            # שמירת רפרנסים לעדכון מהיר בלי לצייר הכל מחדש
            item.ui_lbl_qty = lbl_qty
            item.ui_lbl_tot = lbl_tot

    def change_qty(self, item, delta):
        new_qty = item.qty + delta
        if 0 <= new_qty <= item.max_qty:
            item.qty = new_qty
            # עדכון טקסטים
            if hasattr(item, 'ui_lbl_qty'): item.ui_lbl_qty.configure(text=str(item.qty))
            if hasattr(item, 'ui_lbl_tot'): item.ui_lbl_tot.configure(text=str(int(item.total_weight)))
            self.update_totals()
            self.on_change() # עדכון למערכת הראשית

    def update_totals(self):
        total_w = sum(i.total_weight for i in self.config_list)
        self.lbl_total.configure(text=f"Total Config Wt: {int(total_w):,} Lbs")