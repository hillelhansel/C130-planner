import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, on_planner, on_fleet):
        super().__init__(parent, fg_color="transparent")
        
        # כותרת
        title = ctk.CTkLabel(self, text="C-130J Mission Planner", font=("Arial", 40, "bold"))
        title.pack(pady=(80, 50))
        
        # כפתורים
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()
        
        btn_planner = ctk.CTkButton(
            btn_frame, 
            text="Mission Planner (תכנון)", 
            font=("Arial", 20, "bold"), 
            width=300, 
            height=60,
            corner_radius=10,
            command=on_planner
        )
        btn_planner.pack(pady=15)
        
        btn_fleet = ctk.CTkButton(
            btn_frame, 
            text="Fleet Manager (Chart C)", 
            font=("Arial", 20, "bold"), 
            width=300, 
            height=60,
            corner_radius=10,
            fg_color="#D9534F", 
            hover_color="#C9302C",
            command=on_fleet
        )
        btn_fleet.pack(pady=15)
        
        ctk.CTkLabel(self, text="v2.5 - Stable", text_color="gray").pack(side="bottom", pady=20)