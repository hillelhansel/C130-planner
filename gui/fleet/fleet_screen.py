import customtkinter as ctk
import tkinter.filedialog as filedialog
from tkinter import messagebox 
from datetime import datetime
import json
from services.fleet_service import FleetService
from core.models import UpdateItem, ConfigItem
from gui.fleet.components.fleet_tables import ConfigTable, UpdatesTable
from gui.fleet.components.fleet_summary import SummaryPanel

class FleetScreen(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="#1a1a1a")
        self.on_back = on_back
        self.service = FleetService()
        self.aircraft = None
        self.current_tail = None

        # 1. Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color="#333", height=50)
        self.top_bar.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(self.top_bar, text="<< Main Menu", width=100, command=on_back, fg_color="#555").pack(side="left", padx=10)
        
        self.tail_btns = {}
        for t in self.service.get_all_tail_numbers():
            btn = ctk.CTkButton(self.top_bar, text=t, width=60, font=("Arial", 14, "bold"), fg_color="#444", 
                                command=lambda x=t: self.load_tail(x))
            btn.pack(side="left", padx=2)
            self.tail_btns[t] = btn

        # 2. Info Bar
        self.info_bar = ctk.CTkFrame(self, fg_color="#2b2b2b", height=50)
        self.info_bar.pack(fill="x", padx=10, pady=5)
        
        self.btn_save = ctk.CTkButton(self.info_bar, text="Save Data (Export)", fg_color="green", width=160, command=self.save_as_file)
        self.btn_save.pack(side="left", padx=10)
        
        self.en_updater = self._add_field("Updater:", 110)
        self.en_date = self._add_field("Date:", 90)
        self.en_reason = self._add_field("Reason:", 200)
        
        self.lbl_idx = ctk.CTkLabel(self.info_bar, text="Update #1", font=("Arial", 14, "bold"), text_color="cyan")
        self.lbl_idx.pack(side="right", padx=20)

        # 3. Main Split
        split = ctk.CTkFrame(self, fg_color="transparent")
        split.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- LEFT: Configuration ---
        config_frame = ctk.CTkFrame(split, fg_color="transparent")
        config_frame.pack(side="left", fill="both", expand=True, padx=(0,5))
        
        ctk.CTkLabel(config_frame, text="Configuration Update", font=("Arial", 18, "bold"), text_color="#E0a800").pack(pady=(5,5))
        
        # Table
        self.config_table = ConfigTable(config_frame, self.on_config_change, self.delete_config_item)
        self.config_table.pack(fill="both", expand=True)
        
        ctk.CTkButton(config_frame, text="+ Add Config Item", fg_color="#444", hover_color="#666", 
                      command=self.popup_add_config).pack(fill="x", pady=5)

        # --- RIGHT: Structural Updates ---
        updates_frame = ctk.CTkFrame(split, fg_color="transparent")
        updates_frame.pack(side="right", fill="both", expand=True, padx=(5,0))
        
        ctk.CTkLabel(updates_frame, text="Structural Updates", font=("Arial", 18, "bold")).pack(pady=(5,5))
        
        self.updates_table = UpdatesTable(updates_frame)
        self.updates_table.pack(fill="both", expand=True)
        
        btns = ctk.CTkFrame(updates_frame, fg_color="transparent")
        btns.pack(fill="x", pady=5)
        ctk.CTkButton(btns, text="+ Structural Update", fg_color="#3B8ED0", width=140, command=self.popup_add_update).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Item Catalog", fg_color="#555", width=120, command=lambda: self.popup_catalog(None)).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Weighing Update", fg_color="#D9534F", width=120, command=self.popup_weighing).pack(side="left", padx=5)
        
        self.summary = SummaryPanel(updates_frame)
        self.summary.pack(fill="x", pady=10)

        if self.tail_btns: self.load_tail(list(self.tail_btns.keys())[0])

    def _add_field(self, txt, w):
        f = ctk.CTkFrame(self.info_bar, fg_color="transparent")
        f.pack(side="left", padx=5)
        ctk.CTkLabel(f, text=txt, font=("Arial", 11)).pack(side="left", padx=2)
        e = ctk.CTkEntry(f, width=w)
        e.pack(side="left", padx=2)
        return e

    def load_tail(self, tail):
        # 1. שמירה זמנית בזיכרון של המטוס הקודם
        if self.aircraft:
            self._sync_header_fields()
            self.service.update_cache_only(self.aircraft)
            
        # 2. עדכון ויזואלי של הכפתור
        for t, b in self.tail_btns.items():
            b.configure(fg_color="#3B8ED0" if t == tail else "#444")
            
        self.current_tail = tail
        self.aircraft = self.service.get_aircraft(tail)
        
        # 3. עדכון שדות כותרת
        self.lbl_idx.configure(text=f"Update #{self.aircraft.current_update_index}")
        self.en_updater.delete(0, "end"); self.en_updater.insert(0, self.aircraft.last_updater_name)
        self.en_date.delete(0, "end"); self.en_date.insert(0, self.aircraft.last_update_date or datetime.now().strftime("%d/%m/%Y"))
        self.en_reason.delete(0, "end"); self.en_reason.insert(0, self.aircraft.update_nature)
        
        # 4. עדכון מהיר של הטבלאות (ללא בניה מחדש של ה-GUI!)
        self.config_table.load_data(self.aircraft.config_items) # השתנה ל-load_data
        
        self.updates_table.refresh(self.aircraft)
        self.summary.update(self.aircraft)

    def _sync_header_fields(self):
        if not self.aircraft: return
        self.aircraft.last_updater_name = self.en_updater.get()
        self.aircraft.last_update_date = self.en_date.get()
        self.aircraft.update_nature = self.en_reason.get()

    def on_config_change(self, idx, delta):
        # עדכון לוגי
        item = self.aircraft.config_items[idx]
        new_val = item.qty_in_plane + delta
        if 0 <= new_val <= item.full_qty:
            item.qty_in_plane = new_val
            # עדכון ויזואלי מהיר (Binding)
            self.config_table.load_data(self.aircraft.config_items)
            self.summary.update(self.aircraft)

    def delete_config_item(self, idx):
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            return
            
        if 0 <= idx < len(self.aircraft.config_items):
            self.aircraft.config_items.pop(idx)
            self.service.update_cache_only(self.aircraft)
            # בגלל מחיקה, צריך רענון מלא של השורות
            self.config_table.load_data(self.aircraft.config_items)
            self.summary.update(self.aircraft)

    def save_as_file(self):
        updater = self.en_updater.get().strip()
        reason = self.en_reason.get().strip()
        
        if not updater or not reason:
            messagebox.showerror("Validation Error", "Please fill in 'Updater' name and 'Reason' before saving.")
            return

        if not messagebox.askyesno("Confirm Save", "Are you sure you want to save and export data?"):
            return

        self._sync_header_fields()
        default_name = f"{self.current_tail}-ChartC-{self.aircraft.current_update_index}"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            initialfile=default_name,
            title="Save Aircraft Data"
        )
        
        if filename:
            try:
                if filename.endswith(".xlsx"):
                    self.service.export_to_excel(self.aircraft, filename)
                else:
                    data = self.service._serialize_aircraft(self.aircraft)
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                
                self.aircraft.current_update_index += 1
                self.service.save_aircraft(self.aircraft)
                self.load_tail(self.current_tail)
                
                messagebox.showinfo("Success", "Data saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    # --- Popups ---
    # הפופאפים נשארים אותו דבר, הם לא משפיעים על המהירות הכללית
    def popup_add_config(self):
        d = ctk.CTkToplevel(self)
        d.title("Add Config Item")
        d.geometry("300x350")
        d.transient(self); d.grab_set()
        ctk.CTkLabel(d, text="New Item Details", font=("Arial", 14, "bold")).pack(pady=10)
        ents = {}
        fields = [("Item Name", "name"), ("Unit Weight", "wt"), ("Standard Qty (Max)", "qty"), ("Arm (LS)", "ls")]
        for txt, key in fields:
            row = ctk.CTkFrame(d, fg_color="transparent"); row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=txt, width=120, anchor="w").pack(side="left")
            e = ctk.CTkEntry(row); e.pack(side="right", fill="x", expand=True)
            ents[key] = e
        def add():
            try:
                nm = ents["name"].get()
                wt = float(ents["wt"].get())
                qty = int(ents["qty"].get())
                ls = float(ents["ls"].get())
                if nm:
                    new_item = ConfigItem(category="General", name=nm, weight_per_unit=wt, full_qty=qty, qty_in_plane=qty, ls=ls)
                    self.aircraft.config_items.append(new_item)
                    self.service.update_cache_only(self.aircraft)
                    self.config_table.load_data(self.aircraft.config_items) # שינוי ל-load_data
                    self.summary.update(self.aircraft)
                    d.destroy()
            except: pass
        ctk.CTkButton(d, text="Add", command=add, fg_color="green").pack(pady=20)

    # שאר הפופאפים (popup_add_update, popup_weighing, popup_catalog) - העתק מהגרסה הקודמת, ללא שינוי.
    def popup_add_update(self):
        d = ctk.CTkToplevel(self)
        d.title("Structural Update")
        d.geometry("350x450")
        d.transient(self); d.grab_set()
        
        ctk.CTkLabel(d, text="Add Structural Update", font=("Arial", 16, "bold"), text_color="#3B8ED0").pack(pady=10)
        
        f_meta = ctk.CTkFrame(d, fg_color="transparent"); f_meta.pack(fill="x", padx=20, pady=5)
        f_n = ctk.CTkFrame(f_meta, fg_color="transparent"); f_n.pack(side="left", fill="x", expand=True, padx=(0,5))
        ctk.CTkLabel(f_n, text="Updater", font=("Arial", 10)).pack(anchor="w")
        e_name = ctk.CTkEntry(f_n); e_name.pack(fill="x"); e_name.insert(0, self.en_updater.get())
        f_d = ctk.CTkFrame(f_meta, fg_color="transparent"); f_d.pack(side="right", fill="x", expand=True, padx=(5,0))
        ctk.CTkLabel(f_d, text="Date", font=("Arial", 10)).pack(anchor="w")
        e_date = ctk.CTkEntry(f_d); e_date.pack(fill="x"); e_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        fields = {"Name": e_name, "Date": e_date}
        ctk.CTkLabel(d, text="Item Description", font=("Arial", 12, "bold")).pack(pady=(15,0), padx=25, anchor="w")
        row_desc = ctk.CTkFrame(d, fg_color="transparent"); row_desc.pack(fill="x", padx=20)
        e_desc = ctk.CTkEntry(row_desc); e_desc.pack(side="left", fill="x", expand=True, padx=(0,5))
        btn_cat = ctk.CTkButton(row_desc, text="...", width=30, fg_color="#555", command=lambda: self.popup_catalog(on_catalog_select, parent_win=d))
        btn_cat.pack(side="right")
        fields["Desc"] = e_desc
        def on_catalog_select(name, wt, arm):
            e_desc.delete(0, "end"); e_desc.insert(0, name)
            fields["Weight"].delete(0, "end"); fields["Weight"].insert(0, str(wt))
            fields["Arm"].delete(0, "end"); fields["Arm"].insert(0, str(arm))
            d.focus_force()
        for txt, key in [("Weight (Lbs)", "Weight"), ("Arm (LS)", "Arm")]:
            ctk.CTkLabel(d, text=txt).pack(anchor="w", padx=25, pady=(5,0))
            e = ctk.CTkEntry(d); e.pack(fill="x", padx=20)
            fields[key] = e
        op_var = ctk.StringVar(value="add")
        f_op = ctk.CTkFrame(d, fg_color="transparent"); f_op.pack(pady=15)
        ctk.CTkRadioButton(f_op, text="Add (+)", variable=op_var, value="add").pack(side="left", padx=10)
        ctk.CTkRadioButton(f_op, text="Remove (-)", variable=op_var, value="remove").pack(side="left", padx=10)
        def confirm():
            try:
                wt = float(fields["Weight"].get())
                if op_var.get() == "remove": wt = -wt
                arm = float(fields["Arm"].get())
                u = UpdateItem(date=fields["Date"].get(), adjuster=fields["Name"].get(), description=fields["Desc"].get(), weight_change=wt, arm_change=arm, moment_change=(wt*arm)/1000.0)
                self.aircraft.update_items.append(u)
                self.service.update_cache_only(self.aircraft)
                self.updates_table.refresh(self.aircraft)
                self.summary.update(self.aircraft)
                d.destroy()
            except: pass
        ctk.CTkButton(d, text="Confirm & Add", command=confirm, fg_color="green").pack(pady=10)

    def popup_weighing(self):
        d = ctk.CTkToplevel(self)
        d.title("Weighing Update")
        d.geometry("300x380")
        d.transient(self); d.grab_set()
        ctk.CTkLabel(d, text="WARNING: Resets History!", text_color="red", font=("Arial", 12, "bold")).pack(pady=10)
        ents = {}
        fr = ctk.CTkFrame(d, fg_color="transparent"); fr.pack(fill="x", padx=20)
        f_n = ctk.CTkFrame(fr, fg_color="transparent"); f_n.pack(side="left", fill="x", expand=True, padx=(0,5))
        ctk.CTkLabel(f_n, text="Updater", font=("Arial", 10)).pack(anchor="w")
        e_n = ctk.CTkEntry(f_n); e_n.pack(fill="x"); e_n.insert(0, self.en_updater.get())
        f_d = ctk.CTkFrame(fr, fg_color="transparent"); f_d.pack(side="right", fill="x", expand=True, padx=(5,0))
        ctk.CTkLabel(f_d, text="Date", font=("Arial", 10)).pack(anchor="w")
        e_d = ctk.CTkEntry(f_d); e_d.pack(fill="x"); e_d.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ents["date"]=e_d; ents["name"]=e_n
        for k in ["Weight", "Arm", "Moment"]:
            ctk.CTkLabel(d, text=k).pack(anchor="w", padx=20, pady=(5,0))
            e = ctk.CTkEntry(d); e.pack(fill="x", padx=20)
            ents[k] = e
        def ok():
            try:
                self.aircraft.weighing_weight = float(ents["Weight"].get())
                self.aircraft.weighing_arm = float(ents["Arm"].get())
                self.aircraft.weighing_moment = float(ents["Moment"].get())
                self.aircraft.update_items = []
                self.aircraft.current_update_index = 1
                self.aircraft.last_updater_name = ents["name"].get()
                self.aircraft.last_update_date = ents["date"].get()
                self.aircraft.update_nature = "Periodic Weighing"
                self.service.update_cache_only(self.aircraft)
                self.load_tail(self.current_tail)
                d.destroy()
            except: pass
        ctk.CTkButton(d, text="Reset & Save", fg_color="red", command=ok).pack(pady=20)

    def popup_catalog(self, select_callback=None, parent_win=None):
        master = parent_win if parent_win else self
        d = ctk.CTkToplevel(master)
        d.title("Item Catalog")
        d.geometry("400x500")
        d.transient(master); d.grab_set() 
        scroll = ctk.CTkScrollableFrame(d)
        scroll.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        def refresh_list():
            for w in scroll.winfo_children(): w.destroy()
            for item in self.service.get_updates_catalog():
                f = ctk.CTkFrame(scroll, fg_color="#333", corner_radius=6)
                f.pack(fill="x", pady=2)
                if select_callback:
                    cmd = lambda i=item: [select_callback(i['name'], i['weight'], i['arm']), d.destroy()]
                    ctk.CTkButton(f, text="Select", width=60, height=24, fg_color="#3B8ED0", command=cmd).pack(side="left", padx=5)
                ctk.CTkLabel(f, text=item['name'], font=("Arial", 12, "bold"), anchor="w").pack(side="left", padx=10)
                info = f"Wt: {item['weight']} | LS: {item['arm']}"
                ctk.CTkLabel(f, text=info, text_color="gray", font=("Arial", 11)).pack(side="right", padx=5)
        add_f = ctk.CTkFrame(d, fg_color="#2b2b2b", border_color="gray", border_width=1)
        add_f.pack(side="bottom", fill="x", padx=5, pady=5)
        ctk.CTkLabel(add_f, text="Add New Item:", font=("Arial", 12, "bold")).pack(pady=5)
        new_ents = {}
        r1 = ctk.CTkFrame(add_f, fg_color="transparent"); r1.pack(fill="x", padx=5)
        new_ents["Name"] = ctk.CTkEntry(r1, placeholder_text="Item Name"); new_ents["Name"].pack(fill="x")
        r2 = ctk.CTkFrame(add_f, fg_color="transparent"); r2.pack(fill="x", pady=5, padx=5)
        ctk.CTkButton(r2, text="Save", width=80, fg_color="green", command=lambda: self.add_cat_item(new_ents, refresh_list)).pack(side="right")
        new_ents["Wt"] = ctk.CTkEntry(r2, width=80, placeholder_text="Weight"); new_ents["Wt"].pack(side="left", padx=2)
        new_ents["Arm"] = ctk.CTkEntry(r2, width=80, placeholder_text="Arm"); new_ents["Arm"].pack(side="left", padx=2)
        refresh_list()

    def add_cat_item(self, ents, cb):
        try:
            n = ents["Name"].get(); w = float(ents["Wt"].get()); a = float(ents["Arm"].get())
            if n:
                self.service.add_to_updates_catalog(n, w, a)
                cb()
                ents["Name"].delete(0,"end"); ents["Wt"].delete(0,"end"); ents["Arm"].delete(0,"end")
        except: pass