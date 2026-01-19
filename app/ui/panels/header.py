import customtkinter as ctk

class HeaderSection:
    def __init__(self, parent, mgr):
        self.mgr = mgr
        f = ctk.CTkFrame(parent, fg_color="transparent"); f.pack(fill="x", pady=10)
        
        ctk.CTkLabel(f, text="TAIL:").pack(side="left")
        self.et = ctk.CTkEntry(f, width=50); self.et.insert(0,"661"); self.et.pack(side="left")
        
        ctk.CTkLabel(f, text="MSN:").pack(side="left", padx=5)
        self.em = ctk.CTkEntry(f, width=80); self.em.pack(side="left")
        
        ctk.CTkButton(f, text="UPD", width=40, command=self.update).pack(side="right")

    def update(self):
        self.mgr.update_header(self.et.get(), self.em.get())