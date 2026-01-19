import customtkinter as ctk
from app.ui.panels.base import BaseSection

class ManifestPanel(BaseSection):
    def __init__(self, parent, mgr, refresh_cb):
        super().__init__(parent, "רשימת העמסה (Manifest)", mgr, refresh_cb)
        
        self.list_frame = ctk.CTkScrollableFrame(self.content_frame, height=150)
        self.list_frame.pack(fill="both", expand=True, pady=5)
        
        self.refresh()

    def refresh(self):
        # ניקוי
        for w in self.list_frame.winfo_children(): w.destroy()
        
        # 1. הצגת צוות
        if self.mgr.logic.crew:
            ctk.CTkLabel(self.list_frame, text="-- צוות ונוסעים --", text_color="#3B8ED0").pack(anchor="w")
            for i, p in enumerate(self.mgr.logic.crew):
                self.create_row(i, p, "crew")

        # 2. הצגת מטען
        if self.mgr.logic.payload:
            ctk.CTkLabel(self.list_frame, text="-- מטען --", text_color="#2CC985").pack(anchor="w", pady=(5,0))
            for i, p in enumerate(self.mgr.logic.payload):
                self.create_row(i, p, "payload")

    def create_row(self, index, item, item_type):
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # שם ומשקל
        txt = f"{item.name} ({item.weight} lbs)"
        if hasattr(item, 'count') and item.count > 1:
            txt += f" x{item.count}"
            
        ctk.CTkLabel(row, text=txt, anchor="w").pack(side="left", padx=5)
        
        # מיקום (Station)
        station = getattr(item, 'station', 0)
        ctk.CTkLabel(row, text=f"@ {station}", text_color="gray").pack(side="left", padx=5)
        
        # כפתור מחיקה
        ctk.CTkButton(row, text="X", width=20, height=20, fg_color="transparent", text_color="red", hover_color="#440000",
                      command=lambda: self.delete_item(index, item_type)).pack(side="right", padx=5)

    def delete_item(self, index, item_type):
        if item_type == "crew":
            self.mgr.remove_crew(index)
        else:
            self.mgr.remove_payload(index)