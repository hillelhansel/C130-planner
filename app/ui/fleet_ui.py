import customtkinter as ctk
import os
from datetime import datetime
from app.data import DataManager, TAIL_NUMBERS, DEFAULT_CONFIG_ITEMS
from core.models import UpdateItem

# --- Helper ---
def fix_text(text):
    if text is None: return ""
    return str(text)

# --- Dialogs ---
class NewWeighingDialog(ctk.CTkToplevel):
    def __init__(self, parent, current_w, current_a, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("עדכון שקילה בסיסית")
        self.geometry("400x450")
        self.transient(parent)
        self.grab_set()
        
        ctk.CTkLabel(self, text="!זהירות: פעולה זו תאפס את כל השינויים", text_color="red", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.en_date = ctk.CTkEntry(self, placeholder_text="תאריך", justify="right")
        self.en_date.pack(pady=5)
        self.en_date.insert(0, datetime.now().strftime("%d/%m/%y"))
        
        self.en_name = ctk.CTkEntry(self, placeholder_text="שם המבצע", justify="right")
        self.en_name.pack(pady=5)

        self.en_w = ctk.CTkEntry(self, placeholder_text="(Lbs) משקל בסיס", justify="center")
        self.en_w.pack(pady=5)
        self.en_w.insert(0, str(current_w))
        
        self.calc_mode = ctk.StringVar(value="Arm")
        r_frame = ctk.CTkFrame(self, fg_color="transparent")
        r_frame.pack(pady=5)
        ctk.CTkRadioButton(r_frame, text="(Arm) לפי זרוע", variable=self.calc_mode, value="Arm").pack(side="right", padx=10)
        ctk.CTkRadioButton(r_frame, text="(Mom) לפי מומנט", variable=self.calc_mode, value="Mom").pack(side="left", padx=10)
        
        self.en_val = ctk.CTkEntry(self, placeholder_text="ערך", justify="center")
        self.en_val.pack(pady=5)
        self.en_val.insert(0, str(current_a))
        
        ctk.CTkButton(self, text="אשר ואיפוס מלא", fg_color="red", font=("Arial", 14, "bold"), command=self.save).pack(pady=20)

    def save(self):
        try:
            w = float(self.en_w.get())
            val = float(self.en_val.get())
            date = self.en_date.get()
            name = self.en_name.get()
            if self.calc_mode.get() == "Arm":
                a = val
                m = (w * a) / 1000.0
            else:
                m = val
                a = (m * 1000.0) / w if w != 0 else 0
            self.callback(w, a, m, date, name)
        except: pass
        finally: self.destroy()

class AddUpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("הוספת עדכון")
        self.geometry("400x550")
        self.transient(parent)
        self.grab_set()
        self.db = DataManager()
        
        ctk.CTkLabel(self, text="פרטי עדכון חדש", font=("Arial", 16, "bold")).pack(pady=10)
        self.type_var = ctk.StringVar(value="Install")
        type_frame = ctk.CTkFrame(self, fg_color="transparent")
        type_frame.pack(pady=5)
        ctk.CTkRadioButton(type_frame, text="(+) התקנה", variable=self.type_var, value="Install", text_color="green").pack(side="right", padx=20)
        ctk.CTkRadioButton(type_frame, text="(-) הסרה", variable=self.type_var, value="Remove", text_color="red").pack(side="left", padx=20)
        
        ctk.CTkLabel(self, text=":(אופציונלי) בחר רכיב מרשימה").pack(pady=(10,0))
        comp_names = ["- בחר רכיב -"] + self.db.get_component_names()
        self.comp_menu = ctk.CTkOptionMenu(self, values=comp_names, command=self.on_comp_select)
        self.comp_menu.pack(pady=5)

        self.en_date = ctk.CTkEntry(self, placeholder_text="תאריך", justify="right")
        self.en_date.pack(pady=5)
        self.en_date.insert(0, datetime.now().strftime("%d/%m/%y"))
        self.en_adj = ctk.CTkEntry(self, placeholder_text="מבצע", justify="right")
        self.en_adj.pack(pady=5)
        self.en_desc = ctk.CTkEntry(self, placeholder_text="תיאור העדכון", justify="right")
        self.en_desc.pack(pady=5)
        self.en_w = ctk.CTkEntry(self, placeholder_text="(Lbs) משקל", justify="center")
        self.en_w.pack(pady=5)
        self.en_a = ctk.CTkEntry(self, placeholder_text="(In) זרוע", justify="center")
        self.en_a.pack(pady=5)
        ctk.CTkButton(self, text="שמור והוסף", fg_color="green", font=("Arial", 14, "bold"), command=self.save).pack(pady=20)

    def on_comp_select(self, choice):
        if choice == "- בחר רכיב -": return
        for item in DEFAULT_CONFIG_ITEMS:
            if item["name"] == choice:
                self.en_desc.delete(0, "end"); self.en_desc.insert(0, item["name"])
                self.en_w.delete(0, "end"); self.en_w.insert(0, str(item["weight_per_unit"]))
                self.en_a.delete(0, "end"); self.en_a.insert(0, str(item["ls"]))
                return

    def save(self):
        try:
            w = float(self.en_w.get())
            a = float(self.en_a.get())
            if self.type_var.get() == "Remove": w = -abs(w)
            else: w = abs(w)
            m = (w * a) / 1000.0
            self.callback(self.en_date.get(), self.en_adj.get(), self.en_desc.get(), w, a, m)
        except ValueError: pass
        finally: self.destroy()

# --- Table ---
class ExcelTable(ctk.CTkFrame):
    def __init__(self, parent, headers, widths, alignments=None):
        super().__init__(parent, fg_color="transparent") # רקע שקוף למסגרת
        self.headers = headers
        self.widths = widths
        self.rows_ui = [] 
        self.alignments = alignments if alignments else ["center"] * len(headers)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#444444", corner_radius=10, height=35)
        self.header_frame.pack(fill="x", pady=(0, 2))
        self.header_frame.pack_propagate(False)
        
        for i, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.header_frame, text=text, width=widths[i], font=("Arial", 12, "bold"), text_color="white", anchor="center")
            lbl.pack(side="right", padx=1)
            
        # Body
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll.pack(fill="both", expand=True)
        
        # Footer
        self.footer_frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10, height=35)
        self.footer_frame.pack(fill="x", pady=(2, 0))
        self.footer_frame.pack_propagate(False)
        self.footer_labels = [] 

    def set_data(self, data_rows, edit_col_idx=None, edit_callback=None):
        while len(self.rows_ui) < len(data_rows):
            self._create_new_row_ui(edit_col_idx, edit_callback)
        for i in range(len(data_rows), len(self.rows_ui)):
            self.rows_ui[i]["frame"].pack_forget()
            
        for i, row_data in enumerate(data_rows):
            values = row_data["values"]
            colors = row_data.get("colors", ["white"] * len(values))
            item_ref = row_data.get("item_ref", None)
            
            ui_row = self.rows_ui[i]
            ui_row["frame"].pack(fill="x", pady=1) 
            
            if edit_col_idx is not None:
                ui_row["btn_plus"].configure(command=lambda r=item_ref: edit_callback(r, 1))
                ui_row["btn_minus"].configure(command=lambda r=item_ref: edit_callback(r, -1))
                entry = ui_row["widgets"][edit_col_idx]
                def on_enter(event, r=item_ref, e=entry):
                    try:
                        new_val = int(e.get())
                        delta = new_val - r.qty_in_plane
                        edit_callback(r, delta)
                    except: pass
                entry.bind("<Return>", on_enter)

            for j, val in enumerate(values):
                widget = ui_row["widgets"][j]
                if isinstance(widget, ctk.CTkEntry):
                    current_val = widget.get()
                    if current_val != str(val):
                        widget.delete(0, "end")
                        widget.insert(0, str(val))
                else:
                    widget.configure(text=str(val), text_color=colors[j])

    def _create_new_row_ui(self, edit_col_idx, edit_callback):
        row_frame = ctk.CTkFrame(self.scroll, fg_color="#2b2b2b", corner_radius=6, height=30)
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)
        
        widgets = []
        btn_plus = None
        btn_minus = None
        
        for i in range(len(self.widths)):
            w = self.widths[i]
            align = self.alignments[i]
            anchor = "e" if align == "right" else "center"
            
            if edit_col_idx is not None and i == edit_col_idx:
                cell = ctk.CTkFrame(row_frame, fg_color="transparent", width=w, height=25)
                cell.pack(side="right", padx=1)
                bp = ctk.CTkButton(cell, text="+", width=20, height=20, fg_color="#444444", hover_color="green")
                bp.pack(side="right", padx=1)
                en = ctk.CTkEntry(cell, width=35, height=20, font=("Arial", 11), justify="center")
                en.pack(side="right", padx=1)
                bm = ctk.CTkButton(cell, text="-", width=20, height=20, fg_color="#444444", hover_color="red")
                bm.pack(side="right", padx=1)
                widgets.append(en)
                btn_plus = bp
                btn_minus = bm
            else:
                lbl = ctk.CTkLabel(row_frame, text="", width=w, font=("Arial", 11), text_color="white", anchor=anchor)
                lbl.pack(side="right", padx=1)
                widgets.append(lbl)
                
        self.rows_ui.append({"frame": row_frame, "widgets": widgets, "btn_plus": btn_plus, "btn_minus": btn_minus})

    def set_footer(self, values):
        if not self.footer_labels:
            for i, val in enumerate(values):
                align = self.alignments[i]
                anchor = "e" if align == "right" else "center"
                lbl = ctk.CTkLabel(self.footer_frame, text=str(val), width=self.widths[i], font=("Arial", 12, "bold"), text_color="cyan", anchor=anchor)
                lbl.pack(side="right", padx=1)
                self.footer_labels.append(lbl)
        else:
            for i, val in enumerate(values):
                self.footer_labels[i].configure(text=str(val))
    
    def clear(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for w in self.footer_frame.winfo_children(): w.destroy()
        self.rows_ui = []
        self.footer_labels = []

# --- Main Screen ---
class FleetManagerScreen(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="#1a1a1a")
        self.db = DataManager()
        self.on_back = on_back
        self.aircraft_data = None
        self.current_tail = "661"
        
        # --- Top Bar ---
        top_bar = ctk.CTkFrame(self, height=40, fg_color="#333333", corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkButton(top_bar, text="חזרה למסך הבית", width=120, command=on_back).pack(side="right", padx=10, pady=5)
        ctk.CTkLabel(top_bar, text="Chart C - Fleet Manager", font=("Arial", 20, "bold")).pack(side="left", padx=20)
        
        # --- Selector ---
        self.ac_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.ac_frame.pack(fill="x", padx=10, pady=5)
        self.ac_buttons = {}
        for tail in TAIL_NUMBERS:
            btn = ctk.CTkButton(self.ac_frame, text=tail, width=70, height=40, font=("Arial", 14, "bold"), fg_color="#444444", command=lambda t=tail: self.load_tail(t))
            btn.pack(side="right", padx=5)
            self.ac_buttons[tail] = btn
            
        # --- Header Info ---
        self.header_info_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", border_width=1, border_color="gray", corner_radius=10)
        self.header_info_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.header_info_frame, text=":עדכון מס").pack(side="right", padx=5)
        self.lbl_idx = ctk.CTkLabel(self.header_info_frame, text="1", font=("Arial", 14, "bold"), text_color="cyan"); self.lbl_idx.pack(side="right", padx=5)
        ctk.CTkLabel(self.header_info_frame, text=":מהות העדכון").pack(side="right", padx=5)
        self.en_nature = ctk.CTkEntry(self.header_info_frame, width=250, justify="right"); self.en_nature.pack(side="right", padx=5)
        ctk.CTkLabel(self.header_info_frame, text=":שם מעדכן").pack(side="right", padx=5)
        self.en_updater = ctk.CTkEntry(self.header_info_frame, width=150, justify="right"); self.en_updater.pack(side="right", padx=5)
        ctk.CTkLabel(self.header_info_frame, text=":תאריך").pack(side="right", padx=5)
        self.en_upd_date = ctk.CTkEntry(self.header_info_frame, width=100, justify="center"); self.en_upd_date.pack(side="right", padx=5)
        ctk.CTkButton(self.header_info_frame, text="שמור והפק דוח", fg_color="#d9534f", command=self.save_and_export).pack(side="left", padx=20, pady=5)

        # --- Main Layout ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=10, pady=10) # מרווח חיצוני
        
        self.main_content.grid_columnconfigure(0, weight=4) 
        self.main_content.grid_columnconfigure(1, weight=6) 
        self.main_content.grid_rowconfigure(0, weight=1)

        # --- LEFT CONTAINER ---
        self.left_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5)) # מרווח קטן בין ימין לשמאל
        self.left_container.grid_rowconfigure(0, weight=1)
        self.left_container.grid_rowconfigure(1, weight=0)

        # Updates
        self.updates_frame = ctk.CTkFrame(self.left_container, border_width=1, border_color="gray", corner_radius=10)
        self.updates_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        
        hdr = ctk.CTkFrame(self.updates_frame, corner_radius=10, fg_color="transparent")
        hdr.pack(fill="x", pady=5)
        ctk.CTkButton(hdr, text="עדכון שקילה", width=100, fg_color="red", command=self.open_weighing_dialog).pack(side="left", padx=5)
        ctk.CTkButton(hdr, text="עדכון מואז +", width=100, fg_color="green", command=self.open_update_dialog).pack(side="left", padx=5)
        ctk.CTkLabel(hdr, text="שינויים ועדכונים", font=("Arial", 16, "bold")).pack(side="right", padx=10)
        
        l_cols = ["תאריך", "מבצע", "תיאור", "משקל", "זרוע", "מומנט"]
        l_w = [80, 80, 200, 60, 60, 70]
        l_align = ["center", "center", "right", "center", "center", "center"]
        self.table_updates = ExcelTable(self.updates_frame, l_cols, l_w, l_align)
        self.table_updates.pack(fill="both", expand=True, padx=5, pady=5)

        # Summary
        self.summary_frame = ctk.CTkFrame(self.left_container, height=120, border_width=1, border_color="gray", corner_radius=10)
        self.summary_frame.grid(row=1, column=0, sticky="ew")
        
        # --- RIGHT CONTAINER ---
        self.right_container = ctk.CTkFrame(self.main_content, border_width=1, border_color="gray", corner_radius=10)
        self.right_container.grid(row=0, column=1, sticky="nsew", padx=(5, 0)) # מרווח קטן
        
        ctk.CTkLabel(self.right_container, text="תצורה (Configuration)", font=("Arial", 16, "bold")).pack(fill="x", pady=5)
        r_cols = ["קטגוריה", "פריט", "משקל יח'", "תקן מלא", "במטוס", "הוסר", "משקל שהוסר", "LS", "מומנט"]
        r_w = [110, 150, 60, 60, 100, 50, 90, 60, 70] 
        r_align = ["right", "right", "center", "center", "center", "center", "center", "center", "center"]
        self.table_config = ExcelTable(self.right_container, r_cols, r_w, r_align)
        self.table_config.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_tail(TAIL_NUMBERS[0])

    def load_tail(self, tail):
        self.table_config.clear()
        self.table_updates.clear()
        self.current_tail = tail
        self.aircraft_data = self.db.get_aircraft_data(tail)
        for t, btn in self.ac_buttons.items():
            if t == tail: btn.configure(fg_color="#1f6aa5", border_color="white", border_width=2)
            else: btn.configure(fg_color="#444444", border_width=0)
        
        ad = self.aircraft_data
        self.lbl_idx.configure(text=str(ad.current_update_index))
        self.en_nature.delete(0, "end"); self.en_nature.insert(0, ad.update_nature)
        self.en_updater.delete(0, "end"); self.en_updater.insert(0, ad.last_updater_name)
        date_str = ad.last_update_date if ad.last_update_date else datetime.now().strftime("%d/%m/%y")
        self.en_upd_date.delete(0, "end"); self.en_upd_date.insert(0, date_str)
        self.render_full_ui()

    def render_full_ui(self):
        self.update_totals()
        ad = self.aircraft_data
        config_rows = []
        tot_rem_w = 0
        tot_rem_m = 0
        
        for item in ad.config_items:
            rem_w = (item.full_qty - item.qty_in_plane) * item.weight_per_unit
            rem_m = (rem_w * item.ls) / 1000.0
            tot_rem_w += rem_w
            tot_rem_m += rem_m
            col_rem = "red" if (item.full_qty - item.qty_in_plane) > 0 else "gray"
            vals = [item.category, item.name, item.weight_per_unit, item.full_qty, item.qty_in_plane, 
                    item.full_qty - item.qty_in_plane, f"{rem_w:.1f}", item.ls, f"{rem_m:.2f}"]
            colors = ["white"]*5 + [col_rem] + ["white"]*3
            config_rows.append({"values": vals, "colors": colors, "item_ref": item})
            
        self.table_config.set_data(config_rows, edit_col_idx=4, edit_callback=self.change_qty)
        self.table_config.set_footer(["", "", "", "", "", "", f"{tot_rem_w:,.1f}", "", f"{tot_rem_m:,.2f}"])

        update_rows = []
        update_rows.append({"values": ["-", "שקילה", "משקל בסיס", ad.weighing_weight, ad.weighing_arm, f"{ad.weighing_moment:.2f}"], "colors": ["gray"]*6})
        for u in ad.update_items:
            col_w = "green" if u.weight_change >= 0 else "red"
            update_rows.append({"values": [u.date, u.adjuster, u.description, u.weight_change, u.arm_change, u.moment_change], "colors": ["white"]*3 + [col_w] + ["white"]*2})
        self.table_updates.set_data(update_rows)

    def change_qty(self, item, delta):
        new = item.qty_in_plane + delta
        if 0 <= new <= item.full_qty:
            item.qty_in_plane = new
            self.db.save_aircraft_data(self.aircraft_data)
            self.render_full_ui() 

    def open_update_dialog(self): AddUpdateDialog(self, self.add_update)

    def add_update(self, d, a, desc, w, arm, mom):
        self.aircraft_data.update_items.append(UpdateItem(d, a, desc, w, arm, mom))
        self.db.save_aircraft_data(self.aircraft_data)
        self.render_full_ui()

    def open_weighing_dialog(self):
        ad = self.aircraft_data
        NewWeighingDialog(self, ad.weighing_weight, ad.weighing_arm, self.update_weighing_callback)

    def update_weighing_callback(self, new_w, new_a, new_m, date, name):
        ad = self.aircraft_data
        ad.weighing_weight = new_w
        ad.weighing_arm = new_a
        ad.weighing_moment = new_m
        if date: ad.last_update_date = date
        if name: ad.last_updater_name = name
        ad.update_items = []
        for item in ad.config_items: item.qty_in_plane = item.full_qty
        self.db.save_aircraft_data(ad)
        self.en_upd_date.delete(0, "end"); self.en_upd_date.insert(0, date)
        self.en_updater.delete(0, "end"); self.en_updater.insert(0, name)
        self.render_full_ui()

    def update_totals(self):
        ad = self.aircraft_data
        for w in self.summary_frame.winfo_children(): w.destroy()
        grid = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=5)
        headers = ["מומנט", "זרוע", "משקל", "תיאור"]
        for c, h in enumerate(headers):
            ctk.CTkLabel(grid, text=h, font=("Arial", 14, "bold"), width=120).grid(row=0, column=c, padx=5)
        
        basic_mom_disp = ad.basic_moment_raw / 1000.0
        rows = [
            ("משקל שקילה", ad.weighing_weight, ad.weighing_arm, ad.weighing_moment),
            ("תצורה הפחתות", -ad.total_removed_weight, "-", -ad.total_removed_moment),
            ("מצטברים עדכונים", ad.total_updates_weight, "-", ad.total_updates_moment),
            ("משקל בסיסי בפועל", ad.basic_weight, f"{ad.basic_arm_calc:.2f}", f"{basic_mom_disp:.2f}")
        ]
        for r, (desc, w, arm, mom) in enumerate(rows):
            fg = "cyan" if r == 3 else "white"
            vals = [mom, arm, w, desc]
            for c, v in enumerate(vals):
                 val_str = f"{v:,.1f}" if isinstance(v, (int, float)) else str(v)
                 ctk.CTkLabel(grid, text=val_str, text_color=fg).grid(row=r+1, column=c, padx=5)

    def save_and_export(self):
        ad = self.aircraft_data
        ad.last_update_date = self.en_upd_date.get()
        ad.last_updater_name = self.en_updater.get()
        ad.update_nature = self.en_nature.get()
        idx = ad.current_update_index
        filename = f"CHART C - {ad.tail_number} - CHANGE {idx}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"CHART C - {ad.tail_number}\nIndex: {idx}\nDate: {ad.last_update_date}\n\nBasic Weight: {ad.basic_weight}")
            ad.current_update_index += 1
            self.db.save_aircraft_data(ad)
            self.lbl_idx.configure(text=str(ad.current_update_index))
            lbl = ctk.CTkLabel(self, text=f"Saved: {filename}", text_color="green")
            lbl.place(relx=0.5, rely=0.9, anchor="center")
            self.after(2000, lbl.destroy)
        except: pass