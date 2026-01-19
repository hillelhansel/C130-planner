import customtkinter as ctk
from app.ui.menu import MainMenu
from app.ui.fleet_ui import FleetManagerScreen

# ייבוא המתכנן המקורי שלך (MissionView)
# אנו משתמשים ב-try למקרה שיש בעיה בקובץ, כדי שהתוכנה לא תקרוס מיד
try:
    from app.ui.mission_view import MissionView
except ImportError as e:
    print(f"Error loading MissionView: {e}")
    MissionView = None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("C-130J Mission Planner")
        self.geometry("1200x800")
        
        # פתיחה במסך מלא
        self.after(0, lambda: self.state('zoomed'))
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_menu()

    def show_menu(self):
        self.clear_frame()
        MainMenu(
            self.container, 
            on_fleet=self.show_fleet_manager, 
            on_planner=self.show_planner,
            on_cargo_db=self.show_cargo_db
        ).pack(fill="both", expand=True)

    def show_fleet_manager(self):
        self.clear_frame()
        # טעינת מסך ניהול הצי החדש (Chart C)
        FleetManagerScreen(self.container, self.show_menu).pack(fill="both", expand=True)

    def show_planner(self):
        self.clear_frame()
        if MissionView:
            # טעינת מסך התכנון המקורי והמורכב שלך
            # אנו מעבירים את self.show_menu כ-callback לכפתור חזרה
            MissionView(self.container, on_back=self.show_menu).pack(fill="both", expand=True)
        else:
            # במקרה של שגיאה בטעינת הקובץ המקורי
            err_lbl = ctk.CTkLabel(self.container, text="שגיאה בטעינת mission_view.py\nודא שהקובץ קיים ב-app/ui", font=("Arial", 20), text_color="red")
            err_lbl.pack(expand=True)
            ctk.CTkButton(self.container, text="חזרה", command=self.show_menu).pack(pady=20)

    def show_cargo_db(self):
        # מסך זמני לאופציה השלישית
        self.clear_frame()
        ctk.CTkLabel(self.container, text="Cargo Database\n(Under Construction)", font=("Arial", 30)).pack(expand=True)
        ctk.CTkButton(self.container, text="חזרה לתפריט", command=self.show_menu).pack(pady=20)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()