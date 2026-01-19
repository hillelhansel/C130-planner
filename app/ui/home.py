# app/ui/home.py
import customtkinter as ctk

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, on_plan, on_fleet, on_catalog):
        super().__init__(parent, fg_color="transparent")
        
        # כותרת ראשית
        ctk.CTkLabel(self, text="C130J-30 FLEET PLANNER", font=("Arial", 32, "bold"), text_color="#1f6aa5").pack(pady=(80, 10))
        ctk.CTkLabel(self, text="Mission Planning & Fleet Management System", font=("Arial", 16)).pack(pady=(0, 50))

        # מסגרת לכפתורים במרכז
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        # כפתור 1: תכנון משימה
        self.create_card(btn_frame, "MISSION PLANNER", "Create and manage load plans", "green", on_plan)
        
        # כפתור 2: ניהול צי מטוסים
        self.create_card(btn_frame, "FLEET MANAGER", "Manage tail numbers & weights", "#1f6aa5", on_fleet)
        
        # כפתור 3: קטלוג מטענים
        self.create_card(btn_frame, "CATALOG DB", "Update cargo items database", "#FFA500", on_catalog)

    def create_card(self, parent, title, subtitle, color, command):
        """פונקציית עזר ליצירת כפתור גדול ויפה"""
        btn = ctk.CTkButton(parent, text=f"{title}\n{subtitle}", command=command,
                             width=350, height=100, fg_color=color, hover_color=color,
                             font=("Arial", 20, "bold"), corner_radius=15)
        btn.pack(pady=15)