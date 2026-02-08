import customtkinter as ctk
from gui.planner.panels.base_panel import BasePanel

class BasicPanel(BasePanel):
    def __init__(self, parent, mgr):
        # שינוי: ה-title מועבר כאן ל-super, לא מתקבל מבחוץ
        super().__init__(parent, "1. BASIC WEIGHT", mgr, start_open=True)
        
        r = ctk.CTkFrame(self.content, fg_color="transparent")
        r.pack(fill="x", pady=5)
        
        ctk.CTkLabel(r, text="Weight:").pack(side="left", padx=2)
        self.ew = ctk.CTkEntry(r, width=70)
        self.ew.pack(side="left", padx=2)
        
        ctk.CTkLabel(r, text="Arm:").pack(side="left", padx=2)
        self.ea = ctk.CTkEntry(r, width=50)
        self.ea.pack(side="left", padx=2)
        
        ctk.CTkButton(r, text="SET", width=40, fg_color="#444").pack(side="left", padx=5)
        
        self.lbl_rem = ctk.CTkLabel(self.content, text="Removals: 0 lbs", text_color="#ff5555", anchor="w")
        self.lbl_rem.pack(fill="x", padx=5)

    def update_view(self, data):
        if self.focus_get() not in [self.ew, self.ea]:
            self.ew.delete(0, "end"); self.ew.insert(0, str(int(data['basic_w'])))
            self.ea.delete(0, "end"); self.ea.insert(0, "723.0") # זמני
            
            ac = self.mgr.aircraft
            self.lbl_rem.configure(text=f"Removals: -{int(ac.total_removed_weight)} lbs")