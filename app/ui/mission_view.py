import customtkinter as ctk
from app.state import MissionStateManager
from app.ui.panels.container import ControlPanel 
from app.ui.diagram import AircraftDiagram
from app.ui.charts import ChartsView
from app.data import DataManager

class MissionView(ctk.CTkFrame):
    def __init__(self, parent, on_back=None, mgr=None, tail_num="661"):
        super().__init__(parent, fg_color="transparent")
        
        # טעינת נתונים
        db = DataManager()
        aircraft_data = db.get_aircraft_data(tail_num)
        
        self.mgr = mgr if mgr else MissionStateManager(tail_number=tail_num)
        
        # עדכון משקל בסיס ומומנט
        if hasattr(self.mgr, 'logic'):
            self.mgr.logic.basic_weight = aircraft_data.basic_weight
            self.mgr.logic.basic_moment = aircraft_data.basic_moment_raw
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # כפתור חזרה (חשוב!)
        if on_back:
            back_btn = ctk.CTkButton(self, text="<< חזרה לתפריט", command=on_back, 
                                     width=120, height=30, fg_color="#444444", hover_color="#666666")
            back_btn.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 0))

        # תפריטים
        self.control_panel = ControlPanel(self, self.mgr, self.refresh_all)
        self.control_panel.grid(row=1, column=0, rowspan=2, sticky="nswe", pady=(5, 0))

        # צד ימין
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=1, column=1, rowspan=2, sticky="nswe", padx=5, pady=5)
        
        # סרגל לגים
        self.plan_bar = ctk.CTkFrame(self.right_frame, fg_color="#2b2b2b", height=40)
        self.plan_bar.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(self.plan_bar, text="Active Leg:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.plan_selector = ctk.CTkOptionMenu(self.plan_bar, values=[], command=self.on_switch_plan, width=150)
        self.plan_selector.pack(side="left", padx=5)
        
        ctk.CTkButton(self.plan_bar, text="Rename", width=60, fg_color="#555555", command=self.popup_rename).pack(side="left", padx=5)
        ctk.CTkButton(self.plan_bar, text="+ New Leg", width=80, fg_color="green", command=self.popup_add_plan).pack(side="right", padx=10)

        # אזור תצוגה
        self.plane_view = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.plane_view.pack(fill="both", expand=True)
        
        self.top_area = ctk.CTkFrame(self.plane_view, fg_color="transparent")
        self.top_area.pack(side="top", fill="both", expand=True)
        
        self.lbl_status = ctk.CTkLabel(self.top_area, text="INIT...", font=("Consolas", 16, "bold"))
        self.lbl_status.pack(side="top", pady=5)
        
        self.diagram = AircraftDiagram(self.top_area, self.mgr, 
                                       self.control_panel.load_for_edit, 
                                       self.mgr.notify)
        self.diagram.pack(fill="both", expand=True)

        self.bottom_area = ctk.CTkFrame(self.plane_view, height=280, fg_color="#2b2b2b")
        self.bottom_area.pack(side="bottom", fill="x", pady=5)
        self.bottom_area.pack_propagate(False)
        self.charts = ChartsView(self.bottom_area)
        self.charts.pack(fill="both", expand=True)

        self.update_plan_selector()
        self.mgr.subscribe(self.on_data_update)
        self.mgr.notify()

    def update_plan_selector(self):
        names = self.mgr.get_plan_names()
        self.plan_selector.configure(values=names)
        self.plan_selector.set(self.mgr.active_plan.name)

    def on_switch_plan(self, choice):
        names = self.mgr.get_plan_names()
        if choice in names:
            idx = names.index(choice)
            self.mgr.set_active_plan(idx)
            self.control_panel.header.em.delete(0, "end")
            self.control_panel.header.em.insert(0, choice)
            self.control_panel.fuel.update_ui()
            self.control_panel.crew.render_list()
            self.control_panel.config_sec.refresh() 

    def popup_add_plan(self):
        dialog = ctk.CTkInputDialog(text="Enter Name for New Plan/Leg:", title="New Plan")
        name = dialog.get_input()
        if name:
            self.mgr.add_plan(name)
            self.update_plan_selector()

    def popup_rename(self):
        dialog = ctk.CTkInputDialog(text="Rename Current Plan:", title="Rename")
        new_name = dialog.get_input()
        if new_name:
            self.mgr.rename_active_plan(new_name)
            self.update_plan_selector()

    def on_data_update(self, mgr, data):
        self.control_panel.render_manifest()
        self.control_panel.update_displays(0, 0) 
        txt = f"BASIC: {int(data['basic_w']):,} | OP: {int(data['op_w']):,} | ZFW: {int(data['zfw']):,} | GW: {int(data['gw']):,} | CG: {data['cg']:.1f} | MAC: {data['mac']:.1f}%"
        self.lbl_status.configure(text=txt)
        self.charts.update_data(data['gw'], data['zfw'], data['fuel_w'], data['mac'])
        self.diagram.draw()

    def refresh_all(self):
        self.mgr.notify()