import customtkinter as ctk
from app.ui.panels.base import BaseSection

# שיניתי את השם ל-ManifestSection כדי שיתאים למה ש-container.py מחפש
class ManifestSection(BaseSection):
    def __init__(self, parent, mgr, load_cb):
        # load_cb הוא הפונקציה load_for_edit שמועברת מה-container
        super().__init__(parent, "רשימת העמסה (Manifest)", mgr, None)
        self.load_callback = load_cb
        
        self.list_frame = ctk.CTkScrollableFrame(self.content_frame, height=150)
        self.list_frame.pack(fill="both", expand=True, pady=5)
        
        self.refresh()

    # הוספתי את הפונקציה render כי container.py קורא לה
    def render(self):
        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        # 1. הצגת צוות
        if self.mgr.logic.crew:
            ctk.CTkLabel(self.list_frame, text="-- צוות ונוסעים --", text_color="#3B8ED0", font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
            for i, p in enumerate(self.mgr.logic.crew):
                self.create_row(i, p, "crew")

        # 2. הצגת מטען
        if self.mgr.logic.payload:
            ctk.CTkLabel(self.list_frame, text="-- מטען --", text_color="#2CC985", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5,0), padx=5)
            for i, p in enumerate(self.mgr.logic.payload):
                self.create_row(i, p, "payload")

    def create_row(self, index, item, item_type):
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # שם ומשקל
        txt = f"{item.name} ({item.weight} lbs)"
        if hasattr(item, 'count') and item.count > 1:
            txt += f" x{item.count}"
            
        # כפתור לחיץ לעריכה (טוען לאדיטור הכתום)
        btn = ctk.CTkButton(row, text=txt, fg_color="transparent", text_color="white", anchor="w",
                            font=("Arial", 12), hover_color="#444444",
                            command=lambda: self.load_callback(item))
        btn.pack(side="left", fill="x", expand=True)
        
        # מיקום (Station)
        station = getattr(item, 'station', 0)
        ctk.CTkLabel(row, text=f"@ {station}", text_color="gray", width=50).pack(side="left", padx=5)
        
        # כפתור מחיקה
        ctk.CTkButton(row, text="X", width=25, height=25, fg_color="transparent", text_color="#ff5555", hover_color="#440000",
                      font=("Arial", 12, "bold"),
                      command=lambda: self.delete_item(index, item_type)).pack(side="right", padx=5)

    def delete_item(self, index, item_type):
        if item_type == "crew":
            self.mgr.remove_crew(index)
        else:
            self.mgr.remove_payload(index)