import customtkinter as ctk
from gui.planner.panels.base_panel import BasePanel
from core.models import CargoItem
from core.fleet_constants import COMPARTMENT_DEFS

class CargoPanel(BasePanel):
    def __init__(self, parent, mgr, on_edit_request):
        super().__init__(parent, "4. CARGO & PAYLOAD", mgr, start_open=True)
        self.on_edit_request = on_edit_request
        self.presets = self.mgr.get_cargo_presets()
        
        # שורה 1: סוג ותא
        r1 = ctk.CTkFrame(self.content, fg_color="transparent"); r1.pack(fill="x", pady=2)
        
        self.cat_var = ctk.StringVar(value="General")
        self.cb_cat = ctk.CTkComboBox(r1, values=list(self.presets.keys()), width=140, command=self.on_cat)
        self.cb_cat.pack(side="left", padx=2)
        
        self.comp_var = ctk.StringVar(value="Manual")
        comps = ["Manual"] + [c[0] for c in COMPARTMENT_DEFS]
        ctk.CTkComboBox(r1, values=comps, width=80, variable=self.comp_var, command=self.on_comp).pack(side="left", padx=2)

        # שורה 2: נתונים
        r2 = ctk.CTkFrame(self.content, fg_color="transparent"); r2.pack(fill="x", pady=2)
        self.en_name = self._mk(r2, "Name", 80)
        self.en_wt = self._mk(r2, "Wt", 50)
        self.en_st = self._mk(r2, "Station", 50)

        # שורה 3: מידות
        r3 = ctk.CTkFrame(self.content, fg_color="transparent"); r3.pack(fill="x", pady=2)
        self.en_len = self._mk(r3, "L", 40)
        self.en_wid = self._mk(r3, "W", 40)
        
        # סליידר מטרי
        self.met_fr = ctk.CTkFrame(self.content, fg_color="transparent")
        self.sl_met = ctk.CTkSlider(self.met_fr, from_=8, to=32, number_of_steps=6, command=self.on_met)
        self.lbl_met = ctk.CTkLabel(self.met_fr, text="8 ft")
        self.sl_met.pack(side="left", fill="x", expand=True); self.lbl_met.pack(side="right")

        ctk.CTkButton(r3, text="ADD", width=50, fg_color="green", command=self.add).pack(side="right", padx=5)
        
        self.scroll = ctk.CTkScrollableFrame(self.content, height=180); self.scroll.pack(fill="both", expand=True)

    def _mk(self, p, ph, w):
        e = ctk.CTkEntry(p, placeholder_text=ph, width=w); e.pack(side="left", padx=1)
        return e

    def on_cat(self, cat):
        self.met_fr.pack_forget()
        d = self.presets.get(cat, {})
        
        if cat != "General": self.en_name.delete(0,"end"); self.en_name.insert(0, cat)
        if d.get("wt"): self.en_wt.delete(0,"end"); self.en_wt.insert(0, str(d["wt"]))
        
        if cat == "Metric Pallet":
            self.met_fr.pack(fill="x", pady=2, after=self.content.winfo_children()[1])
            self.on_met(8)
            self._lock(self.en_len); self._lock(self.en_wid)
        else:
            self._unlock(self.en_len); self.en_len.delete(0,"end"); self.en_len.insert(0, str(d.get("l", 0)))
            self._unlock(self.en_wid); self.en_wid.delete(0,"end"); self.en_wid.insert(0, str(d.get("w", 0)))
            
            if cat != "General": # נעילה למטענים מוגדרים
                self._lock(self.en_len); self._lock(self.en_wid)

    def on_met(self, val):
        ft = int(val); self.lbl_met.configure(text=f"{ft} ft")
        self._unlock(self.en_len); self.en_len.delete(0,"end"); self.en_len.insert(0, str(ft*12)); self._lock(self.en_len)
        self._unlock(self.en_wid); self.en_wid.delete(0,"end"); self.en_wid.insert(0, "108"); self._lock(self.en_wid)

    def _lock(self, e): e.configure(state="disabled")
    def _unlock(self, e): e.configure(state="normal")

    def on_comp(self, c):
        if c == "Manual": return
        for n, s, e in COMPARTMENT_DEFS:
            if n == c: self.en_st.delete(0,"end"); self.en_st.insert(0, str(int((s+e)/2))); break

    def add(self):
        try:
            y = -40 if self.comp_var.get() != "Manual" else 0
            self.mgr.add_cargo(CargoItem(self.en_name.get(), float(self.en_wt.get()), float(self.en_st.get()),
                                         float(self.en_len.get() or 0), float(self.en_wid.get() or 0), 
                                         self.cat_var.get(), y_offset=y))
        except: pass

    def update_view(self, data):
        for w in self.scroll.winfo_children(): w.destroy()
        for i, item in enumerate(self.mgr.payload):
            f = ctk.CTkFrame(self.scroll, fg_color="#333", height=25); f.pack(fill="x", pady=1)
            btn = ctk.CTkButton(f, text=f"{item.name} ({int(item.weight)}) @ {item.station}", anchor="w", fg_color="transparent", height=20, hover_color="#444",
                                command=lambda x=item, idx=i: self.on_edit_request(x, 'cargo', idx))
            btn.pack(side="left", fill="x", expand=True)
            ctk.CTkButton(f, text="X", width=25, height=20, fg_color="transparent", text_color="red", command=lambda idx=i: self.mgr.remove_payload(idx)).pack(side="right")