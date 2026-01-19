import customtkinter as ctk
from .base import BaseSection

class CrewSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        self.section = BaseSection(parent, "2. OPERATING WEIGHT")
        
        ctk.CTkLabel(self.section.content, text="Crew List", font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
        self.crew_frame = ctk.CTkFrame(self.section.content, fg_color="transparent")
        self.crew_frame.pack(fill="x")
        
        self.render_list()
        
        self.lbl_fak = ctk.CTkLabel(self.section.content, text="FAK: 0 Lbs", text_color="green", anchor="w", font=("Arial", 14, "bold"))
        self.lbl_fak.pack(fill="x", padx=5, pady=2)

    def render_list(self):
        for w in self.crew_frame.winfo_children(): w.destroy()
        
        h = ctk.CTkFrame(self.crew_frame, fg_color="transparent"); h.pack(fill="x")
        headers = [("Name", 80), ("Qty", 30), ("Wt", 40), ("LS", 40)]
        for txt, w in headers:
            ctk.CTkLabel(h, text=txt, width=w, anchor="w" if txt=="Name" else "center", font=("Arial", 11, "bold")).pack(side="left")

        for item in self.mgr.crew_list:
            row = ctk.CTkFrame(self.crew_frame, fg_color="transparent"); row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=item.name, width=80, anchor="w").pack(side="left")
            
            is_editable = not item.fixed or item.name == "LM"
            st = "normal" if is_editable else "disabled"
            col = "#333333" if is_editable else "#444444"
            
            e_c = ctk.CTkEntry(row, width=30); e_c.insert(0, str(item.count)); e_c.configure(state=st, fg_color=col); e_c.pack(side="left", padx=1)
            e_w = ctk.CTkEntry(row, width=40); e_w.insert(0, str(int(item.weight))); e_w.configure(state=st, fg_color=col); e_w.pack(side="left", padx=1)
            e_ls = ctk.CTkEntry(row, width=40); e_ls.insert(0, str(int(item.ls))); e_ls.configure(state=st, fg_color=col); e_ls.pack(side="left", padx=1)
            
            if is_editable:
                for e in [e_c, e_w, e_ls]: 
                    e.bind("<FocusOut>", lambda ev, i=item, ec=e_c, ew=e_w, el=e_ls: self.update_crew(i, ec, ew, el))
            
            if not item.fixed and item.name != "LM":
                ctk.CTkButton(row, text="X", width=20, fg_color="red", command=lambda i=item: self.remove_crew(i)).pack(side="left", padx=2)

        # Add Row
        add_row = ctk.CTkFrame(self.crew_frame, fg_color="#444444"); add_row.pack(fill="x", pady=5)
        self.cb_new_name = ctk.CTkComboBox(add_row, values=["OBSERVER", "TECH", "OTHER", "EXTRA PILOT", "EXTRA NAV", "EXTRA LM"], width=80)
        self.cb_new_name.pack(side="left", padx=1)
        self.en_new_cnt = ctk.CTkEntry(add_row, width=30, placeholder_text="Qty"); self.en_new_cnt.pack(side="left", padx=1)
        self.en_new_wt = ctk.CTkEntry(add_row, width=40, placeholder_text="Wt"); self.en_new_wt.pack(side="left", padx=1)
        self.en_new_ls = ctk.CTkEntry(add_row, width=40, placeholder_text="LS"); self.en_new_ls.pack(side="left", padx=1)
        ctk.CTkButton(add_row, text="+", width=20, fg_color="green", command=self.add_crew_inline).pack(side="left", padx=2)

    def add_crew_inline(self):
        try: self.mgr.add_crew_member(self.cb_new_name.get(), float(self.en_new_wt.get()), float(self.en_new_ls.get()), int(self.en_new_cnt.get())); self.render_list()
        except: pass

    def remove_crew(self, item):
        self.mgr.remove_crew_member(item); self.render_list()

    def update_crew(self, item, ec, ew, el):
        try: self.mgr.update_crew_member(item, float(ew.get()), float(el.get()), int(ec.get()))
        except: pass

    def update_display(self, fak_weight):
        self.lbl_fak.configure(text=f"FAK: {int(fak_weight):,} Lbs")