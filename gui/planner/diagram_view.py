import customtkinter as ctk
from core.fleet_constants import COMPARTMENT_DEFS

class DiagramView(ctk.CTkFrame):
    def __init__(self, parent, mgr):
        super().__init__(parent, fg_color="#1a1a1a", height=220)
        self.mgr = mgr
        self.canvas = ctk.CTkCanvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        self.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        if w < 100: return 
        st_start, st_end = 100, 1250 
        scale = w / (st_end - st_start)
        def x(st): return (st - st_start) * scale
        my = self.canvas.winfo_height() / 2
        
        # Aircraft Body (Detailed)
        self.canvas.create_line(x(245), my-40, x(1141), my-40, fill="gray", width=2)
        self.canvas.create_line(x(245), my+40, x(1141), my+40, fill="gray", width=2)
        self.canvas.create_oval(x(160), my-40, x(290), my+40, outline="gray", width=2) # Nose
        self.canvas.create_polygon(x(200), my-25, x(245), my-40, x(245), my-20, x(210), my-15, fill="#3B8ED0", outline="gray") # Cockpit
        self.canvas.create_line(x(1141), my-40, x(1220), my-110, fill="gray", width=2) # Tail
        self.canvas.create_line(x(1141), my+40, x(1190), my+10, fill="gray", width=2) # Ramp
        self.canvas.create_line(x(520), my-40, x(580), my-120, fill="#333", width=2) # Wing L
        self.canvas.create_line(x(680), my-40, x(620), my-120, fill="#333", width=2) # Wing R

        # Compartments
        for n, s, e in COMPARTMENT_DEFS:
            self.canvas.create_line(x(s), my-38, x(s), my+38, fill="#444", dash=(2,4))
            self.canvas.create_text(x((s+e)/2), my+55, text=n, fill="gray", font=("Arial", 9))

        # Payload
        for item in self.mgr.payload:
            l = (item.length or 30) / (st_end-st_start) * w
            wi = ((item.width or 30) / 120) * 80
            xc, yc = x(item.station), my + (item.y_offset * 0.5)
            col = "#3B8ED0" if "Pax" in item.type_code else "#E0a800"
            self.canvas.create_rectangle(xc-l/2, yc-wi/2, xc+l/2, yc+wi/2, fill=col, outline="black")
            if l > 15: self.canvas.create_text(xc, my, text=item.name[:5], font=("Arial", 8, "bold"))

        # Crew
        for m in self.mgr.crew:
            self.canvas.create_oval(x(m.station)-5, my-5, x(m.station)+5, my+5, fill="#5555ff", outline="white")

        # CG
        cg = self.mgr.calculate_current_state()['cg']
        if 200 < cg < 1200:
            self.canvas.create_line(x(cg), my-70, x(cg), my+70, fill="#FF5555", width=2, dash=(6,2))
            self.canvas.create_text(x(cg), my-85, text=f"CG: {cg:.1f}", fill="#FF5555", font=("Arial", 10, "bold"))

    def update_view(self, data): self.draw()