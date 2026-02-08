import customtkinter as ctk
from services.mission_manager import MissionManager
from gui.fleet.components.fleet_tables import ConfigTable

class ShavingPanel(ctk.CTkFrame):
    def __init__(self, parent, mgr: MissionManager, refresh_cb):
        super().__init__(parent, fg_color="transparent")
        self.mgr = mgr
        self.refresh_cb = refresh_cb # פונקציה לרענון התוצאות במסך הראשי
        
        # כותרת
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=10)
        ctk.CTkLabel(header, text="Shaving Form (Mission Configuration)", font=("Arial", 18, "bold")).pack(side="left")
        ctk.CTkLabel(header, text="* Shared for all legs", text_color="gray").pack(side="left", padx=10)
        
        # שימוש בטבלת התצורה הקיימת (ConfigTable)
        # אנו מעבירים לה את הפונקציות שלנו לטיפול בשינויים ומחיקה
        self.table = ConfigTable(self, self.on_config_change, self.on_delete_item)
        self.table.pack(fill="both", expand=True)
        
        # טעינת נתונים ראשונית
        self.reload_data()

    def reload_data(self):
        """טעינת הנתונים מתוך המשימה הנוכחית לטבלה"""
        if self.mgr.current_plan:
            self.table.load_data(self.mgr.current_plan.shaving_config)

    def on_config_change(self, idx, delta):
        """טיפול בלחיצה על +/-"""
        if not self.mgr.current_plan: return
        
        item = self.mgr.current_plan.shaving_config[idx]
        new_val = item.qty_in_plane + delta
        
        if 0 <= new_val <= item.full_qty:
            item.qty_in_plane = new_val
            # עדכון התצוגה בטבלה
            self.table.update_values(self.mgr.current_plan.shaving_config)
            # עדכון המשקלים במסך הראשי
            self.refresh_cb()

    def on_delete_item(self, idx):
        """טיפול במחיקת פריט מרשימת הגילוח"""
        if not self.mgr.current_plan: return
        
        # בטופס גילוח מחיקה = הסרת הפריט מהרשימה (או איפוס)
        # נמחק אותו מהרשימה של המשימה
        if 0 <= idx < len(self.mgr.current_plan.shaving_config):
            self.mgr.current_plan.shaving_config.pop(idx)
            # רענון מלא של הטבלה
            self.table.load_data(self.mgr.current_plan.shaving_config)
            self.refresh_cb()