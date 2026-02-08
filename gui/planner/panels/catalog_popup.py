import customtkinter as ctk
from core.fleet_constants import DEFAULT_CONFIG_ITEMS

class CatalogPopup(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("קטלוג ציוד (Catalog)")
        self.geometry("600x650")
        
        # הופך את החלון למודאלי (חוסם גישה לחלון הראשי עד לסגירה)
        self.transient(parent)
        self.grab_set()
        
        # כותרת
        ctk.CTkLabel(self, text="בחר פריט מהקטלוג", font=("Arial", 18, "bold")).pack(pady=10)
        
        # יצירת טאבים לפי קטגוריות
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ארגון הנתונים: מילון שבו המפתח הוא הקטגוריה והערך הוא רשימת פריטים
        self.cat_map = {}
        
        # מיון הפריטים לקטגוריות
        for item in DEFAULT_CONFIG_ITEMS:
            # שימוש בברירת מחדל 'כללי' אם אין קטגוריה
            cat = item.get("category", "General")
            if cat not in self.cat_map:
                self.cat_map[cat] = []
            self.cat_map[cat].append(item)
            
        # יצירת הטאבים בפועל
        for category, items in self.cat_map.items():
            self.create_category_tab(category, items)

    def create_category_tab(self, category_name, items):
        # הוספת טאב חדש
        tab = self.tab_view.add(category_name)
        
        # מסגרת גלילה בתוך הטאב
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        # יצירת שורה לכל פריט
        for item in items:
            self.create_item_row(scroll, item)

    def create_item_row(self, parent, item):
        # מסגרת לשורה
        card = ctk.CTkFrame(parent, fg_color="#333333", corner_radius=6)
        card.pack(fill="x", pady=2, padx=2)
        
        # שם הפריט
        name_lbl = ctk.CTkLabel(card, text=item['name'], font=("Arial", 12, "bold"), anchor="w")
        name_lbl.pack(side="left", padx=10, pady=5)
        
        # פרטים טכניים (משקל ו-LS)
        info = f"Weight: {item['weight_per_unit']} | Ref LS: {item.get('ls', 0)}"
        ctk.CTkLabel(card, text=info, text_color="gray", font=("Arial", 11)).pack(side="left", padx=10)
        
        # כפתור הוספה
        ctk.CTkButton(card, text="הוסף", width=60, fg_color="#2CC985", hover_color="#26a870",
                      command=lambda i=item: self.on_select(i)).pack(side="right", padx=5, pady=5)

    def on_select(self, item_data):
        # שליחת הנתונים חזרה לפאנל המטען
        # אם אין Station מוגדר, משתמשים ב-LS כברירת מחדל
        station = item_data.get('ls', 500.0)
        
        self.callback(
            name=item_data['name'],
            weight=item_data['weight_per_unit'],
            station=station
        )