import customtkinter as ctk
from tkinter import messagebox
from .base import BaseSection
from app import config

class FuelSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        self.section = BaseSection(parent, "3. FUEL")
        
        top = ctk.CTkFrame(self.section.content, fg_color="transparent"); top.pack(fill="x")
        ctk.CTkLabel(top, text="TOTAL:", font=("Arial", 12, "bold"), text_color="cyan").pack(side="left")
        
        self.total_entry = ctk.CTkEntry(top, width=80); self.total_entry.pack(side="left", padx=10)
        self.total_entry.bind("<Return>", self.on_total_manual)
        
        self.slider = ctk.CTkSlider(self.section.content, from_=0, to=65000, command=self.on_slide)
        self.slider.pack(fill="x", padx=10, pady=5)
        
        grid = ctk.CTkFrame(self.section.content, fg_color="transparent"); grid.pack(fill="x")
        self.f_ents = {}
        tanks = ["Auxiliary", "Inboard", "Outboard", "External"]
        for i, t in enumerate(tanks):
            ctk.CTkLabel(grid, text=t, font=("Arial", 13, "bold")).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5)
            e = ctk.CTkEntry(grid, width=60); e.grid(row=i//2, column=(i%2)*2+1, sticky="e", padx=5)
            e.bind("<Return>", lambda event, t=t: self.on_tank_manual(t))
            e.bind("<FocusOut>", lambda event, t=t: self.on_tank_manual(t))
            self.f_ents[t] = e
        
        self.update_ui()

    def update_ui(self):
        total = sum(self.mgr.fuel_tanks.values())
        self.slider.configure(command=None); self.slider.set(total); self.slider.configure(command=self.on_slide)
        self.total_entry.delete(0, "end"); self.total_entry.insert(0, str(int(total)))
        for t, e in self.f_ents.items():
            val = int(self.mgr.fuel_tanks.get(t, 0))
            e.delete(0, "end"); e.insert(0, str(val)); e.configure(text_color="white")

    def on_slide(self, val): self.mgr.set_total_fuel(val); self.update_ui()
    def on_total_manual(self, e): 
        try: self.mgr.set_total_fuel(float(self.total_entry.get())); self.update_ui()
        except: pass
    
    def on_tank_manual(self, tank_name):
        entry = self.f_ents[tank_name]
        try:
            val = float(entry.get())
            max_cap = config.FUEL_CAPACITIES.get(tank_name, 0)
            if val > max_cap:
                entry.configure(text_color="red"); messagebox.showerror("Error", f"Max {tank_name}: {max_cap}"); val = max_cap
                entry.delete(0, "end"); entry.insert(0, str(int(val)))
            else: entry.configure(text_color="white")
            self.mgr.update_fuel(tank_name, val); self.update_ui()
        except: pass