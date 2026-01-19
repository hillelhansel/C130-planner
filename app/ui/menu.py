import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, on_fleet, on_planner, on_cargo_db):
        super().__init__(parent, fg_color="transparent")
        
        # כותרת ראשית
        ctk.CTkLabel(self, text="C-130J Mission Planner", font=("Arial", 40, "bold")).pack(pady=(80, 50))
        
        # מיכל לכפתורים
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()
        
        # --- כפתור 1: ניהול צי (Fleet Manager) ---
        btn_fleet = ctk.CTkButton(
            btn_frame, 
            text="Fleet Manager (ניהול צי)", 
            font=("Arial", 22, "bold"), 
            width=400, 
            height=70,
            corner_radius=15,
            fg_color="#3B8ED0", 
            hover_color="#36719F",
            command=on_fleet
        )
        btn_fleet.pack(pady=15)
        
        # --- כפתור 2: תכנון משימה (Mission Planner) ---
        btn_planner = ctk.CTkButton(
            btn_frame, 
            text="Mission Planner (תכנון משימה)", 
            font=("Arial", 22, "bold"), 
            width=400, 
            height=70,
            corner_radius=15,
            fg_color="#2CC985", 
            hover_color="#25A96F",
            command=on_planner
        )
        btn_planner.pack(pady=15)
        
        # --- כפתור 3: ספר מטענים (Cargo DB) - עתידי ---
        btn_cargo = ctk.CTkButton(
            btn_frame, 
            text="Cargo Database (ספר מטענים) - בקרוב", 
            font=("Arial", 22, "bold"), 
            width=400, 
            height=70,
            corner_radius=15,
            fg_color="#555555", # אפור כי זה לא פעיל עדיין
            hover_color="#444444",
            state="disabled", # כרגע מושבת
            command=on_cargo_db
        )
        btn_cargo.pack(pady=15)
        
        # כיתוב תחתון
        ctk.CTkLabel(self, text="v3.5 - Full Integration", text_color="gray").pack(side="bottom", pady=20)