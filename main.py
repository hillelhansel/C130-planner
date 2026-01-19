import customtkinter as ctk
from app.ui.menu import MainMenu
from app.ui.fleet_ui import FleetManagerScreen
# שים לב: אנחנו טוענים את MissionView, לא את PlannerScreen!
from app.ui.mission_view import MissionView 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("C-130J Mission Planner")
        self.geometry("1200x800")
        self.after(0, lambda: self.state('zoomed'))
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_menu()

    def show_menu(self):
        self.clear_frame()
        # וודא שהפונקציות מועברות נכון
        MainMenu(self.container, 
                 on_fleet=self.show_fleet_manager, 
                 on_planner=self.show_planner,
                 on_cargo_db=lambda: print("Cargo DB TODO")).pack(fill="both", expand=True)

    def show_planner(self):
        self.clear_frame()
        # כאן התיקון הגדול: MissionView במקום PlannerScreen
        MissionView(self.container, on_back=self.show_menu).pack(fill="both", expand=True)

    def show_fleet_manager(self):
        self.clear_frame()
        FleetManagerScreen(self.container, self.show_menu).pack(fill="both", expand=True)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()