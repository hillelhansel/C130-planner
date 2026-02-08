import customtkinter as ctk

class SummaryPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#2b2b2b", border_width=1, border_color="#444")
        
        ctk.CTkLabel(self, text="Summary", font=("Arial", 16, "bold"), text_color="orange").pack(pady=5)
        
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=10, pady=5)
        for i in range(4): self.grid_frame.grid_columnconfigure(i, weight=1)

        headers = ["", "Weight", "Arm", "Moment"]
        for i, h in enumerate(headers):
            align = "w" if i == 0 else "center"
            ctk.CTkLabel(self.grid_frame, text=h, font=("Arial", 12, "bold"), text_color="gray").grid(row=0, column=i, pady=5, sticky="ew")
            
        self.labels = {}
        self.rows_config = [
            ("weighing", "Weighing Weight"),
            ("config", "Configuration Update"),
            ("updates", "Structural Update"),
            ("total", "BASIC WEIGHT")
        ]
        
        colors = ["white", "#ff5555", "#55ff55", "cyan"]
        
        for idx, (key, title) in enumerate(self.rows_config):
            r = idx + 1
            # שינוי: פונט גדול יותר (15 במקום 13)
            ctk.CTkLabel(self.grid_frame, text=title, font=("Arial", 15, "bold"), text_color=colors[idx], anchor="w").grid(row=r, column=0, sticky="w", padx=10, pady=5)
            
            self.labels[key] = {}
            for c_idx, field in enumerate(["wt", "arm", "mom"]):
                # שינוי: פונט גדול יותר למספרים (15)
                l = ctk.CTkLabel(self.grid_frame, text="0.0", font=("Arial", 15))
                l.grid(row=r, column=c_idx+1)
                self.labels[key][field] = l

    def update(self, ac):
        rem_w = sum((i.full_qty - i.qty_in_plane) * i.weight_per_unit for i in ac.config_items)
        rem_m = sum(((i.full_qty - i.qty_in_plane) * i.weight_per_unit * i.ls) for i in ac.config_items) / 1000.0
        rem_a = (rem_m * 1000) / rem_w if rem_w != 0 else 0
        
        upd_w = sum(u.weight_change for u in ac.update_items)
        upd_m = sum(u.moment_change for u in ac.update_items)
        upd_a = (upd_m * 1000) / upd_w if upd_w != 0 else 0
        
        tot_w = ac.weighing_weight - rem_w + upd_w
        tot_m = ac.weighing_moment - rem_m + upd_m
        tot_a = (tot_m * 1000) / tot_w if tot_w != 0 else 0
        
        self._set("weighing", ac.weighing_weight, ac.weighing_arm, ac.weighing_moment)
        self._set("config", -rem_w, rem_a, -rem_m)
        self._set("updates", upd_w, upd_a, upd_m)
        self._set("total", tot_w, tot_a, tot_m)

    def _set(self, key, w, a, m):
        self.labels[key]["wt"].configure(text=f"{w:,.1f}")
        self.labels[key]["arm"].configure(text=f"{a:.1f}")
        self.labels[key]["mom"].configure(text=f"{m:,.1f}")