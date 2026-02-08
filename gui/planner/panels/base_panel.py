import customtkinter as ctk

class BasePanel(ctk.CTkFrame):
    def __init__(self, parent, title, mission_manager, start_open=False):
        super().__init__(parent, fg_color="transparent")
        self.mgr = mission_manager
        self.is_open = start_open
        
        # כפתור הכותרת (מתפקד כמתג לפתיחה/סגירה)
        self.btn_toggle = ctk.CTkButton(
            self, 
            text=f"▼ {title}" if start_open else f"▶ {title}",
            fg_color="#333333", 
            hover_color="#444444", 
            anchor="w",
            font=("Arial", 12, "bold"),
            command=self.toggle
        )
        self.btn_toggle.pack(fill="x", pady=2)
        
        # תוכן הפאנל (מוסתר או מוצג)
        self.content = ctk.CTkFrame(self, fg_color="#2b2b2b")
        if start_open:
            self.content.pack(fill="x", padx=2, pady=2)

    def toggle(self):
        if self.is_open:
            self.content.pack_forget()
            self.btn_toggle.configure(text=self.btn_toggle.cget("text").replace("▼", "▶"))
            self.is_open = False
        else:
            self.content.pack(fill="x", padx=2, pady=2)
            self.btn_toggle.configure(text=self.btn_toggle.cget("text").replace("▶", "▼"))
            self.is_open = True

    def update_view(self, data):
        """פונקציה שהילדים חייבים לממש"""
        pass