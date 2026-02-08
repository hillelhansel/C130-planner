import customtkinter as ctk

class EditorPanel(ctk.CTkFrame):
    def __init__(self, parent, mgr, on_close):
        # מסגרת כתומה בולטת כמו במקור
        super().__init__(parent, fg_color="#333333", border_color="#E0a800", border_width=2)
        self.mgr = mgr
        self.on_close = on_close
        self.current_item = None
        self.item_type = None 
        self.item_index = -1

        # כותרת
        top = ctk.CTkFrame(self, fg_color="transparent", height=25)
        top.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(top, text="EDIT ITEM", text_color="#E0a800", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(top, text="✕", width=25, height=20, fg_color="transparent", hover_color="#444", command=on_close).pack(side="right")

        # תוכן
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="x", padx=5, pady=5)
        
        # שורה 1: שם ומשקל
        r1 = ctk.CTkFrame(content, fg_color="transparent")
        r1.pack(fill="x", pady=2)
        self.en_name = self._add_field(r1, "Name:", 90)
        self.en_weight = self._add_field(r1, "Wt:", 50)
        
        # שורה 2: מיקום
        r2 = ctk.CTkFrame(content, fg_color="transparent")
        r2.pack(fill="x", pady=2)
        self.en_station = self._add_field(r2, "St:", 50)
        
        # שורה 3: מידות (רק למטען)
        self.dim_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.dim_frame.pack(fill="x", pady=2)
        self.en_len = self._add_field(self.dim_frame, "L:", 40)
        self.en_wid = self._add_field(self.dim_frame, "W:", 40)

        # כפתור שמירה
        ctk.CTkButton(self, text="APPLY CHANGES", fg_color="#E0a800", text_color="black", 
                      height=28, command=self.apply).pack(fill="x", padx=10, pady=10)

    def _add_field(self, parent, txt, w):
        ctk.CTkLabel(parent, text=txt, font=("Arial", 11)).pack(side="left", padx=2)
        e = ctk.CTkEntry(parent, width=w, height=24)
        e.pack(side="left", padx=2)
        return e

    def load_item(self, item, item_type, index):
        self.current_item = item
        self.item_type = item_type
        self.item_index = index
        
        self.en_name.delete(0,"end"); self.en_name.insert(0, item.name)
        self.en_weight.delete(0,"end"); self.en_weight.insert(0, str(item.weight))
        self.en_station.delete(0,"end"); self.en_station.insert(0, str(item.station))
        
        # טיפול במידות
        if item_type == 'cargo':
            self.dim_frame.pack(fill="x", pady=2)
            self.en_len.delete(0,"end"); self.en_len.insert(0, str(item.length))
            self.en_wid.delete(0,"end"); self.en_wid.insert(0, str(item.width))
        else:
            self.dim_frame.pack_forget()

    def apply(self):
        try:
            name = self.en_name.get()
            wt = float(self.en_weight.get())
            st = float(self.en_station.get())
            
            if self.item_type == 'crew':
                self.mgr.update_crew(self.item_index, name, wt, st, self.current_item.count)
            else:
                l = float(self.en_len.get())
                w = float(self.en_wid.get())
                # מעדכן את האובייקט הקיים
                self.current_item.name = name
                self.current_item.weight = wt
                self.current_item.station = st
                self.current_item.length = l
                self.current_item.width = w
                self.mgr.update_cargo(self.item_index, self.current_item)
            
            self.on_close()
        except ValueError: pass