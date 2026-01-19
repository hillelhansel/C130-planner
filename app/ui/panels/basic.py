import customtkinter as ctk
from .base import BaseSection

class BasicWeightSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        self.section = BaseSection(parent, "1. BASIC WEIGHT", start_open=True)
        
        r = ctk.CTkFrame(self.section.content, fg_color="transparent"); r.pack(fill="x")
        
        ctk.CTkLabel(r, text="Wt:").pack(side="left")
        ew = ctk.CTkEntry(r, width=70); ew.insert(0, str(self.mgr.basic_weight)); ew.pack(side="left")
        
        ctk.CTkLabel(r, text="Arm:").pack(side="left", padx=2)
        ea = ctk.CTkEntry(r, width=50); ea.insert(0, str(self.mgr.basic_arm)); ea.pack(side="left")
        
        ctk.CTkButton(r, text="SET", width=40, command=lambda: self.mgr.set_basic_data(ew.get(), ea.get())).pack(side="left", padx=5)
        
        self.lbl_rem = ctk.CTkLabel(self.section.content, text="Removals: 0 Lbs", text_color="#FF6666", anchor="w", font=("Arial", 14, "bold"))
        self.lbl_rem.pack(fill="x", padx=5, pady=2)

    def update_display(self, removals_weight):
        self.lbl_rem.configure(text=f"Removals: {int(removals_weight):,} Lbs")