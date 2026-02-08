import customtkinter as ctk
from gui.planner.panels.base_panel import BasePanel

class CrewPanel(BasePanel):
    def __init__(self, parent, mgr):
        super().__init__(parent, "צוות ונוסעים (Crew)", mgr)
        
        # רשימה נגללת
        self.scroll_list = ctk.CTkScrollableFrame(self.content, height=180, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, pady=5)
        
        # כפתור הוספה
        ctk.CTkButton(self.content, text="+ הוסף נוסע/איש צוות", fg_color="green", 
                      command=self.add_crew_popup).pack(pady=5, fill="x")

    def update_view(self, data):
        # ניקוי ובנייה מחדש
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
            
        for i, member in enumerate(self.mgr.crew):
            self._create_row(i, member)

    def _create_row(self, index, member):
        row = ctk.CTkFrame(self.scroll_list, fg_color="#333333", corner_radius=5)
        row.pack(fill="x", pady=2)
        
        # פרטים
        info_text = f"{member.name}\n{member.weight} lbs  @ St. {member.station}"
        ctk.CTkLabel(row, text=info_text, anchor="w", justify="left", font=("Arial", 11)).pack(side="left", padx=5, pady=2)
        
        # כפתור מחיקה (רק אם לא קבוע)
        if not member.fixed:
            ctk.CTkButton(row, text="X", width=25, height=25, fg_color="transparent", text_color="#ff5555", hover_color="#440000",
                          command=lambda: self.mgr.remove_crew(index)).pack(side="right", padx=5)

    def add_crew_popup(self):
        # דיאלוג הוספה פשוט (אפשר לשדרג לחלון נפרד בהמשך)
        dialog = ctk.CTkInputDialog(text="Format: Name, Weight, Station\nExample: Tech, 200, 245", title="Add Crew")
        res = dialog.get_input()
        if res:
            try:
                parts = res.split(',')
                name = parts[0].strip()
                weight = float(parts[1])
                station = float(parts[2])
                self.mgr.add_crew(name, weight, station)
            except:
                print("Invalid input format")