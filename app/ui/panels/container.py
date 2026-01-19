# app/ui/panels/container.py
import customtkinter as ctk
from .base import EditorPanel
from .header import HeaderSection
from .config_panel import ConfigurationSection # New Import
from .basic import BasicWeightSection
from .crew import CrewSection
from .fuel import FuelSection
from .cargo import CargoSection
from .manifest import ManifestSection

class ControlPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, mission_manager, refresh_callback):
        super().__init__(parent, width=340, corner_radius=0)
        self.mgr = mission_manager
        self.refresh = refresh_callback
        
        self.editor = EditorPanel(self, self.mgr, self.close_editor)
        self.header = HeaderSection(self, self.mgr)
        
        # New Section inserted here
        self.config_sec = ConfigurationSection(self, self.mgr)
        
        self.basic = BasicWeightSection(self, self.mgr)
        self.basic_frame = self.basic.section # Anchor for editor
        
        self.crew = CrewSection(self, self.mgr)
        self.fuel = FuelSection(self, self.mgr)
        self.cargo = CargoSection(self, self.mgr)
        self.manifest = ManifestSection(self, self.mgr, self.load_for_edit)

    def close_editor(self):
        self.editor.pack_forget()

    def load_for_edit(self, item):
        if not item: 
            self.close_editor()
            return
        self.editor.load(item)
        self.editor.pack(fill="x", pady=5, before=self.basic_frame)

    def render_manifest(self):
        self.manifest.render()
    
    def update_displays(self, removals_w, fak_w):
        # רענון טבלת הקונפיגורציה במקרה של החלפת לג
        self.config_sec.refresh()
        
        # פונקציות אלו נשארו לתמיכה, אך המשקל שלהן כרגע מחושב אחרת
        self.basic.update_display(0)
        self.crew.update_display(0)