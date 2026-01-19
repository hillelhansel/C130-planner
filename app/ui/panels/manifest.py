import customtkinter as ctk
from .base import BaseSection

class ManifestSection:
    def __init__(self, parent, mgr, edit_callback):
        self.mgr = mgr
        self.edit_callback = edit_callback
        self.section = BaseSection(parent, "5. MANIFEST")
        self.man_ui = ctk.CTkFrame(self.section.content, fg_color="#333333"); self.man_ui.pack(fill="x")

    def render(self):
        for w in self.man_ui.winfo_children(): w.destroy()
        for item in self.mgr.cargo_list:
            r = ctk.CTkFrame(self.man_ui, fg_color="#444444"); r.pack(fill="x", pady=1)
            ctk.CTkButton(r, text=f"{item.name} | {int(item.weight)}", fg_color="transparent", anchor="w",
                          command=lambda x=item: self.edit_callback(x)).pack(side="left", fill="x", expand=True)