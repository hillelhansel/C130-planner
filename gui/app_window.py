import customtkinter as ctk
from gui.navigation.main_menu import MainMenu
from gui.planner.mission_screen import MissionScreen
from services.mission_manager import MissionManager


class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("C-130J Mission Planner")

        # מצב כהה
        ctk.set_appearance_mode("Dark")

        # === פתיחה במסך מלא ===
        self.after(10, self.maximize_window)

        self.mission_manager = MissionManager()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_menu()

    def maximize_window(self):
        try:
            self.state("zoomed")          # Windows
        except:
            self.attributes("-fullscreen", True)  # Linux / Mac

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_frame()
        MainMenu(
            self.container,
            self.show_planner,
            self.show_fleet
        ).pack(fill="both", expand=True)

    def show_planner(self):
        self.clear_frame()
        MissionScreen(
            self.container,
            self.mission_manager,
            self.show_menu
        ).pack(fill="both", expand=True)

    def show_fleet(self):
        self.clear_frame()
        from gui.fleet.fleet_screen import FleetScreen
        FleetScreen(
            self.container,
            self.show_menu
        ).pack(fill="both", expand=True)
