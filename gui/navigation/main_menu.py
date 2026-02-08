# gui/navigation/main_menu.py
import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, on_planner_click, on_fleet_click):
        super().__init__(parent, fg_color="transparent")
        
        # מרכוז התוכן
        self.center_box = ctk.CTkFrame(self, fg_color="transparent")
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.center_box, text="C-130J Mission Planner", font=("Arial", 32, "bold")).pack(pady=40)
        
        # כפתורים
        btn_config = {"width": 300, "height": 60, "font": ("Arial", 18)}
        
        ctk.CTkButton(self.center_box, text="Mission Planner (תכנון משימה)", 
                      command=on_planner_click, **btn_config).pack(pady=10)
                      
        ctk.CTkButton(self.center_box, text="Fleet Manager (ניהול צי)", 
                      command=on_fleet_click, fg_color="#555555", **btn_config).pack(pady=10)
        
        ctk.CTkButton(self.center_box, text="Cargo Database", 
                      fg_color="#333333", **btn_config).pack(pady=10)