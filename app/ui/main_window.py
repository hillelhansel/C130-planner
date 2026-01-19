# app/ui/main_window.py
import customtkinter as ctk
from app.ui.home import HomeScreen
from app.ui.catalog_ui import CatalogManagerScreen
from app.ui.fleet_ui import FleetManagerScreen
from app.ui.mission_view import MissionView
from app.data import DataManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoadmasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("C130J-30 Fleet Planner System")
        self.geometry("1800x1000")
        
        print("Initializing LoadmasterApp...") # הדפסה לבדיקה

        # טעינת מסד הנתונים
        self.db = DataManager() 

        # יצירת "מיכל" ראשי שבו נחליף את המסכים
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # הפעלה ראשונית - חובה לקרוא לפונקציה הזו
        self.show_home()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_home(self):
        print("Showing Home Screen") # הדפסה לבדיקה
        self.clear_container()
        HomeScreen(self.container, 
                   on_plan=self.show_planner, 
                   on_fleet=self.show_fleet, 
                   on_catalog=self.show_catalog).pack(fill="both", expand=True)

    def show_planner(self):
        self.clear_container()
        
        # מסגרת ראשית לתכנון
        planner_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        planner_frame.pack(fill="both", expand=True)
        
        # סרגל ניווט
        nav = ctk.CTkFrame(planner_frame, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(nav, text="< Home", width=80, fg_color="#444444", command=self.show_home).pack(side="left")
        ctk.CTkLabel(nav, text="MISSION PLANNING", font=("Arial", 16, "bold")).pack(side="left", padx=20)
        ctk.CTkButton(nav, text="+ New Plane", width=100, command=lambda: self.add_tab_logic(self.tabs)).pack(side="right")

        # טאבים
        self.tabs = ctk.CTkTabview(planner_frame)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        
        # טעינת מטוסים
        fleet = self.db.get_fleet()
        if fleet:
            for tail in fleet:
                self.add_tab_logic(self.tabs, tail)
        else:
            self.add_tab_logic(self.tabs, "661")

    def add_tab_logic(self, tabs_widget, name=None):
        if not name: name = f"Plane {len(tabs_widget._tab_dict) + 1}"
        try:
            tabs_widget.add(name)
            MissionView(tabs_widget.tab(name), tail_num=name).pack(fill="both", expand=True)
        except ValueError: pass

    def show_fleet(self):
        self.clear_container()
        FleetManagerScreen(self.container, on_back=self.show_home).pack(fill="both", expand=True)

    def show_catalog(self):
        self.clear_container()
        CatalogManagerScreen(self.container, on_back=self.show_home).pack(fill="both", expand=True)