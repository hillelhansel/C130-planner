import customtkinter as ctk

class BaseSection(ctk.CTkFrame):
    def __init__(self, parent, title, start_open=False):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=5, pady=5)
        self.content = ctk.CTkFrame(self)
        self.btn = ctk.CTkButton(self, text=f"▶ {title}" if not start_open else f"▼ {title}", 
                                 fg_color="#444444", hover_color="#555555", anchor="w",
                                 command=lambda: self.toggle(title))
        self.btn.pack(fill="x")
        if start_open: self.content.pack(fill="x", padx=2, pady=2)
    def toggle(self, title):
        if self.content.winfo_ismapped(): self.content.pack_forget(); self.btn.configure(text=f"▶ {title}")
        else: self.content.pack(fill="x", padx=2, pady=2); self.btn.configure(text=f"▼ {title}")

class EditorPanel(ctk.CTkFrame):
    def __init__(self, parent, state, on_close_callback):
        super().__init__(parent, fg_color="#555555", border_color="orange", border_width=2)
        self.state = state
        self.item = None
        self.on_close = on_close_callback

        ctk.CTkLabel(self, text="QUICK EDIT", text_color="orange", font=("Arial",12,"bold")).pack(pady=2)
        
        # Name
        self.en = ctk.CTkEntry(self, placeholder_text="Name"); self.en.pack(pady=2, padx=5, fill="x")
        
        # Row 1: Weight & LS
        r1 = ctk.CTkFrame(self, fg_color="transparent"); r1.pack(pady=2)
        ctk.CTkLabel(r1, text="Wt:", width=30).pack(side="left")
        self.ew = ctk.CTkEntry(r1, width=60); self.ew.pack(side="left", padx=2)
        ctk.CTkLabel(r1, text="LS:", width=25).pack(side="left")
        self.els = ctk.CTkEntry(r1, width=60); self.els.pack(side="left", padx=2)

        # Row 2: Dimensions (Length & Width)
        r2 = ctk.CTkFrame(self, fg_color="transparent"); r2.pack(pady=2)
        ctk.CTkLabel(r2, text="Len:", width=30).pack(side="left")
        self.elen = ctk.CTkEntry(r2, width=60); self.elen.pack(side="left", padx=2)
        ctk.CTkLabel(r2, text="Wid:", width=25).pack(side="left")
        self.ewid = ctk.CTkEntry(r2, width=60); self.ewid.pack(side="left", padx=2)

        ctk.CTkButton(self, text="APPLY", fg_color="green", command=self.apply).pack(pady=5)

    def load(self, item):
        self.item = item
        self.en.delete(0,"end"); self.en.insert(0, item.name)
        self.ew.delete(0,"end"); self.ew.insert(0, str(int(item.weight)))
        self.els.delete(0,"end"); self.els.insert(0, str(int(item.ls)))
        self.elen.delete(0,"end"); self.elen.insert(0, str(int(item.length)))
        self.ewid.delete(0,"end"); self.ewid.insert(0, str(int(item.width)))

    def apply(self):
        if self.item:
            try: 
                self.state.update_cargo_properties(
                    self.item, 
                    name=self.en.get(), 
                    weight=float(self.ew.get()), 
                    ls=float(self.els.get()),
                    length=float(self.elen.get()),
                    width=float(self.ewid.get())
                )
                if self.on_close: self.on_close()
            except: pass