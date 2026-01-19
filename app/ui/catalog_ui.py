# app/ui/catalog_ui.py
import customtkinter as ctk
from app.data import DataManager

class CatalogManagerScreen(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.db = DataManager()
        self.on_back = on_back
        
        # Header
        h = ctk.CTkFrame(self, height=50); h.pack(fill="x", pady=10)
        ctk.CTkButton(h, text="< Back", width=60, command=on_back).pack(side="left", padx=10)
        ctk.CTkLabel(h, text="CARGO CATALOG DATABASE", font=("Arial", 20, "bold")).pack(side="left", padx=20)

        # Content
        content = ctk.CTkFrame(self); content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left: List
        self.list_frame = ctk.CTkScrollableFrame(content, width=300)
        self.list_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right: Form
        form = ctk.CTkFrame(content); form.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(form, text="Add / Edit Item", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.en_name = ctk.CTkEntry(form, placeholder_text="Item Name"); self.en_name.pack(pady=5)
        self.en_wt = ctk.CTkEntry(form, placeholder_text="Weight (Lbs)"); self.en_wt.pack(pady=5)
        self.en_len = ctk.CTkEntry(form, placeholder_text="Length (Inch)"); self.en_len.pack(pady=5)
        self.en_wid = ctk.CTkEntry(form, placeholder_text="Width (Inch)"); self.en_wid.pack(pady=5)
        self.cb_type = ctk.CTkComboBox(form, values=["Gen", "Pallet", "Metric", "Pax", "Drop"]); self.cb_type.pack(pady=5)
        
        ctk.CTkButton(form, text="SAVE ITEM", fg_color="green", command=self.save_item).pack(pady=20)
        ctk.CTkButton(form, text="DELETE SELECTED", fg_color="red", command=self.delete_item).pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        catalog = self.db.get_catalog()
        for name, data in catalog.items():
            btn = ctk.CTkButton(self.list_frame, text=f"{name} ({data['type']})", 
                                fg_color="transparent", border_width=1, anchor="w",
                                command=lambda n=name, d=data: self.load_form(n, d))
            btn.pack(fill="x", pady=2)

    def load_form(self, name, data):
        self.en_name.delete(0, "end"); self.en_name.insert(0, name)
        self.en_wt.delete(0, "end"); self.en_wt.insert(0, str(data['weight']))
        self.en_len.delete(0, "end"); self.en_len.insert(0, str(data['length']))
        self.en_wid.delete(0, "end"); self.en_wid.insert(0, str(data['width']))
        self.cb_type.set(data['type'])

    def save_item(self):
        try:
            self.db.add_to_catalog(
                self.en_name.get(), float(self.en_wt.get()), 
                float(self.en_len.get()), float(self.en_wid.get()), self.cb_type.get()
            )
            self.refresh_list()
        except: pass

    def delete_item(self):
        self.db.remove_from_catalog(self.en_name.get())
        self.refresh_list()