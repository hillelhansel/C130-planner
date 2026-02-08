import customtkinter as ctk
from core.fleet_constants import DEFAULT_CONFIG_ITEMS

class CatalogPopup(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("קטלוג מטען")
        self.geometry("400x500")
        
        # חיפוש
        self.entry_search = ctk.CTkEntry(self, placeholder_text="חפש פריט...")
        self.entry_search.pack(fill="x", padx=10, pady=10)
        self.entry_search.bind("<KeyRelease>", self.filter_list)
        
        # רשימה
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.items = DEFAULT_CONFIG_ITEMS
        self.refresh(self.items)

    def filter_list(self, event):
        term = self.entry_search.get().lower()
        filtered = [i for i in self.items if term in i['name'].lower()]
        self.refresh(filtered)

    def refresh(self, items):
        for w in self.scroll.winfo_children(): w.destroy()
        
        for item in items:
            btn = ctk.CTkButton(self.scroll, 
                                text=f"{item['name']} - {item['weight_per_unit']} lbs",
                                anchor="w", fg_color="transparent", border_width=1, border_color="#444",
                                command=lambda i=item: self.select_item(i))
            btn.pack(fill="x", pady=2)

    def select_item(self, item_data):
        # ברירת מחדל למיקום (אפשר לשנות אחר כך)
        station = item_data.get('ls', 500) 
        self.callback(item_data['name'], item_data['weight_per_unit'], station)
        self.destroy()