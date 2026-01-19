import customtkinter as ctk
from app.data import DataManager, DEFAULT_ITEMS

class ConfigEditor(ctk.CTkToplevel):
    def __init__(self, parent, mgr, close_cb):
        super().__init__(parent)
        self.mgr = mgr
        self.close_cb = close_cb
        self.db = DataManager()
        self.title("עריכת תצורה מהירה")
        self.geometry("600x500")
        
        self.tail = self.mgr.tail_number
        self.ac_data = self.db.get_aircraft_data(self.tail)
        self.items = self.ac_data.config_items
        
        ctk.CTkLabel(self, text=f"עריכת תצורה - מטוס {self.tail}", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.entries = {}
        
        for i, item in enumerate(self.items):
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=item.name, width=200, anchor="w").pack(side="left", padx=5)
            
            ctk.CTkButton(row, text="-", width=30, fg_color="#D9534F", command=lambda x=item, idx=i: self.change_qty(idx, -1)).pack(side="right", padx=2)
            
            lbl_qty = ctk.CTkLabel(row, text=str(item.qty_in_plane), width=30, font=("Arial", 12, "bold"))
            lbl_qty.pack(side="right", padx=5)
            self.entries[i] = lbl_qty
            
            ctk.CTkButton(row, text="+", width=30, fg_color="#2CC985", command=lambda x=item, idx=i: self.change_qty(idx, 1)).pack(side="right", padx=2)
            
            ctk.CTkLabel(row, text=f"Max: {item.full_qty}", text_color="gray").pack(side="right", padx=10)

        ctk.CTkButton(self, text="שמור וסגור", command=self.save_and_close).pack(pady=10)

    def change_qty(self, idx, delta):
        item = self.items[idx]
        new_qty = item.qty_in_plane + delta
        if 0 <= new_qty <= item.full_qty:
            item.qty_in_plane = new_qty
            self.entries[idx].configure(text=str(new_qty))

    def save_and_close(self):
        self.db.save_aircraft_data(self.ac_data)
        # עדכון הלוגיקה הראשית כדי ששינויי התצורה ישפיעו על הגרפים מיד
        self.mgr.logic.basic_weight = self.ac_data.basic_weight
        self.mgr.logic.basic_moment = self.ac_data.basic_moment_raw
        self.close_cb()
        self.destroy()