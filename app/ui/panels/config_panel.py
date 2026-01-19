import customtkinter as ctk
from app.ui.panels.base import BaseSection
from app.data import DataManager 
from app.ui.panels.config_editor import ConfigEditor

class ConfigPanel(BaseSection):
    def __init__(self, parent, mgr, refresh_cb):
        super().__init__(parent, "תצורה וציוד (Configuration)", mgr, refresh_cb)
        self.db = DataManager()
        
        self.add_header_button("Quick Edit", self.open_editor, fg_color="#D9534F")
        self.grid_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.grid_frame.pack(fill="x", pady=5)
        self.refresh()

    def refresh(self):
        for w in self.grid_frame.winfo_children(): w.destroy()
            
        headers = ["פריט", "משקל", "כמות", 'סה"כ', "L.S"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.grid_frame, text=h, font=("Arial", 11, "bold"), text_color="gray").grid(row=0, column=i, sticky="ew", padx=2)
            
        current_tail = self.mgr.tail_number
        aircraft_data = self.db.get_aircraft_data(current_tail)
        
        row = 1
        total_weight = 0
        
        # גישה לאובייקטים (לא מילונים)
        for item in aircraft_data.config_items:
            if item.qty_in_plane > 0:
                w_total = item.qty_in_plane * item.weight_per_unit
                total_weight += w_total
                
                vals = [item.name, f"{item.weight_per_unit:.1f}", str(item.qty_in_plane), f"{w_total:.1f}", f"{item.ls:.1f}"]
                for i, v in enumerate(vals):
                    ctk.CTkLabel(self.grid_frame, text=v, font=("Arial", 12)).grid(row=row, column=i, sticky="ew", padx=2, pady=1)
                row += 1
        
        ctk.CTkFrame(self.grid_frame, height=1, fg_color="gray").grid(row=row, column=0, columnspan=5, sticky="ew", pady=5)
        row += 1
        ctk.CTkLabel(self.grid_frame, text='סה"כ משקל תצורה:', font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky="e")
        ctk.CTkLabel(self.grid_frame, text=f"{total_weight:,.1f}", font=("Arial", 12, "bold"), text_color="#3B8ED0").grid(row=row, column=3)

    def open_editor(self):
        ConfigEditor(self, self.mgr, self.on_editor_close)

    def on_editor_close(self):
        self.mgr.notify()