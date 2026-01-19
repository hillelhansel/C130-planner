import customtkinter as ctk
from .base import BaseSection
from .config_editor import ConfigEditorPanel

class ConfigurationSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        # מיקום הפאנל: 0. AIRCRAFT CONFIG
        self.section = BaseSection(parent, "0. AIRCRAFT CONFIG", start_open=False)
        
        self.editor = ConfigEditorPanel(self.section.content, self.mgr.current_configuration, 
                                        on_change_callback=self.mgr.notify)
        self.editor.pack(fill="both", expand=True)
        
    def refresh(self):
        # פונקציה שנקראת כשעוברים בין לגים (Plans) כדי לטעון נתונים חדשים
        self.editor.config_list = self.mgr.current_configuration
        self.editor.render_items()
        self.editor.update_totals()