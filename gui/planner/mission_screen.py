import customtkinter as ctk
from gui.planner.panels.fuel_panel import FuelPanel
from gui.planner.panels.crew_panel import CrewPanel
from gui.planner.panels.cargo_panel import CargoPanel
from gui.planner.panels.basic_panel import BasicPanel
from gui.planner.panels.editor_panel import EditorPanel
from gui.planner.diagram_view import DiagramView
from gui.planner.charts_view import ChartsView

class MissionScreen(ctk.CTkFrame):
    def __init__(self, parent, mission_manager, on_back):
        super().__init__(parent, fg_color="transparent")
        self.mgr = mission_manager
        self.on_back = on_back
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Left Panel (400px width)
        self.left = ctk.CTkFrame(self, width=400, corner_radius=0)
        self.left.grid(row=0, column=0, rowspan=2, sticky="nswe")
        self.left.grid_propagate(False)
        
        # Header
        hl = ctk.CTkFrame(self.left, fg_color="transparent")
        hl.pack(fill="x", pady=5)
        ctk.CTkButton(hl, text="<< Menu", width=60, command=self.on_back, fg_color="#444").pack(side="left", padx=5)
        ctk.CTkLabel(hl, text="CONTROL PANEL", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        # Editor Container
        self.edit_cont = ctk.CTkFrame(self.left, fg_color="transparent")
        self.edit_cont.pack(fill="x", padx=5, pady=5)
        self.editor = None

        # Scrollable Panels
        self.scroll = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)
        
        # Load Panels
        self.basic = BasicPanel(self.scroll, self.mgr)
        self.basic.pack(fill="x", pady=2, padx=2)
        self.crew = CrewPanel(self.scroll, self.mgr)
        self.crew.pack(fill="x", pady=2, padx=2)
        self.fuel = FuelPanel(self.scroll, self.mgr)
        self.fuel.pack(fill="x", pady=2, padx=2)
        self.cargo = CargoPanel(self.scroll, self.mgr, self.open_edit)
        self.cargo.pack(fill="x", pady=2, padx=2)
        
        # Right Panel
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=0, column=1, rowspan=2, sticky="nswe", padx=10, pady=10)
        
        # Plan Bar
        pb = ctk.CTkFrame(self.right, fg_color="#2b2b2b", height=40)
        pb.pack(side="top", fill="x", pady=(0, 5))
        ctk.CTkLabel(pb, text="Leg:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.ps = ctk.CTkOptionMenu(pb, values=self.mgr.get_plan_names(), command=self.sw_plan, width=120)
        self.ps.pack(side="left", padx=5)
        ctk.CTkButton(pb, text="+ Leg", width=60, fg_color="green", command=self.add_leg).pack(side="right", padx=10)

        # Status
        self.stat = ctk.CTkLabel(self.right, text="Init...", font=("Consolas", 16, "bold"), text_color="#3B8ED0")
        self.stat.pack(pady=5)

        # Visuals
        self.diag = DiagramView(self.right, self.mgr)
        self.diag.pack(fill="both", expand=True, pady=(0, 10))
        self.charts = ChartsView(ctk.CTkFrame(self.right, height=250, fg_color="#2b2b2b"), self.mgr)
        self.charts.master.pack(side="bottom", fill="x")
        self.charts.pack(fill="both", expand=True)

        self.mgr.subscribe(self.upd)

    def open_edit(self, item, type, idx):
        if self.editor: self.editor.destroy()
        self.editor = EditorPanel(self.edit_cont, self.mgr, self.close_edit)
        self.editor.pack(fill="x")
        self.editor.load_item(item, type, idx)

    def close_edit(self):
        if self.editor: self.editor.destroy(); self.editor = None

    def upd(self, mgr, data):
        if self.ps.cget("values") != self.mgr.get_plan_names(): self.ps.configure(values=self.mgr.get_plan_names())
        self.ps.set(data.get('plan_name', ''))
        self.stat.configure(text=f"GW: {int(data['gw']):,} | CG: {data['cg']:.1f} | MAC: {data['mac']:.1f}% | Fuel: {int(data['fuel_w']):,}")
        for p in [self.basic, self.fuel, self.crew, self.cargo, self.diag, self.charts]: p.update_view(data)

    def sw_plan(self, c): 
        if c in self.mgr.get_plan_names(): self.mgr.set_active_plan(self.mgr.get_plan_names().index(c))
    def add_leg(self): 
        d = ctk.CTkInputDialog(text="Name:", title="New Leg"); r = d.get_input()
        if r: self.mgr.add_plan(r)