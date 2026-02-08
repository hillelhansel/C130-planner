import customtkinter as ctk
from gui.planner.panels.base_panel import BasePanel
from core.fleet_constants import FUEL_CAPACITIES

class FuelPanel(BasePanel):
    def __init__(self, parent, mgr):
        super().__init__(parent, "דלק (Fuel)", mgr)
        
        self.max_fuel = sum(FUEL_CAPACITIES.values())
        
        # סליידר
        self.slider = ctk.CTkSlider(self.content, from_=0, to=self.max_fuel, number_of_steps=500, command=self.on_slider)
        self.slider.pack(fill="x", pady=10)
        
        # שורת הזנה
        row = ctk.CTkFrame(self.content, fg_color="transparent")
        row.pack(fill="x", pady=5)
        
        self.entry = ctk.CTkEntry(row, placeholder_text="Total Lbs")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.entry.bind("<Return>", self.on_entry)
        
        ctk.CTkButton(row, text="עדכן", width=60, command=self.on_entry).pack(side="right")
        
        # תצוגת מיכלים מפורטת
        self.tank_lbls = {}
        tanks_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        tanks_frame.pack(fill="x", pady=5)
        
        for t in ["External", "Auxiliary", "Outboard", "Inboard"]:
            r = ctk.CTkFrame(tanks_frame, fg_color="transparent")
            r.pack(fill="x", pady=1)
            ctk.CTkLabel(r, text=t, width=80, anchor="w", font=("Arial", 11)).pack(side="left")
            l = ctk.CTkLabel(r, text="0", text_color="#3B8ED0", font=("Arial", 11, "bold"))
            l.pack(side="right")
            self.tank_lbls[t] = l

    def on_slider(self, value):
        self.mgr.set_fuel(value)

    def on_entry(self, event=None):
        try:
            val = float(self.entry.get())
            val = min(val, self.max_fuel)
            self.mgr.set_fuel(val)
        except ValueError:
            pass

    def update_view(self, data):
        fuel = data['fuel_w']
        self.slider.set(fuel)
        
        if self.focus_get() != self.entry:
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(fuel)))
            
        tanks = data.get('tanks', {})
        for k, v in tanks.items():
            if k in self.tank_lbls:
                self.tank_lbls[k].configure(text=f"{int(v):,}")