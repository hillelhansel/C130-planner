# app/state.py
import copy
from app import config
from app.models import PlaneState, PlanState, CrewItem, CargoItem
from app.logic import Calculator
from app.data import DataManager

class MissionStateManager:
    def __init__(self, tail_number="661"):
        self._observers = []
        self.db = DataManager()
        
        # 1. טעינת אובייקט AircraftData מה-DB
        aircraft_data = self.db.get_aircraft_data(tail_number)
        
        if aircraft_data:
            # שימוש במשקל הבסיסי המחושב מהטופס
            base_w = aircraft_data.basic_weight
            base_a = aircraft_data.basic_arm_calc
            # שימוש ברשימת הקונפיגורציה הקיימת
            base_config = copy.deepcopy(aircraft_data.config_items)
        else:
            # Fallback למקרה שאין מטוס כזה
            base_w = config.DEFAULT_BASIC_WEIGHT
            base_a = config.DEFAULT_BASIC_ARM
            base_config = []

        self.plane = PlaneState(
            tail_number=tail_number,
            basic_weight=base_w,
            basic_arm=base_a,
            base_configuration=base_config
        )
        
        self.add_plan("Plan A")

    def add_plan(self, name):
        fuel = Calculator.distribute_fuel(28000.0)
        crew = [
            CrewItem("Pilots", 200, 160, "Seat", "front", count=2, fixed=True),
            CrewItem("Navigator", 200, 180, "Seat", "center", count=1, fixed=True),
            CrewItem("LM", 200, 400, "LM", "free", count=1, fixed=False) 
        ]
        
        # Deep Copy כדי ששינויים בלג אחד לא ישפיעו על אחרים
        plan_config = copy.deepcopy(self.plane.base_configuration)
        
        self.plane.plans.append(PlanState(name=name, fuel_tanks=fuel, crew_list=crew, configuration=plan_config))
        self.plane.active_plan_index = len(self.plane.plans) - 1
        self.notify()

    def set_active_plan(self, index):
        if 0 <= index < len(self.plane.plans):
            self.plane.active_plan_index = index
            self.notify()

    def rename_active_plan(self, new_name):
        self.active_plan.name = new_name
        self.notify()

    def get_plan_names(self): return [p.name for p in self.plane.plans]

    @property
    def active_plan(self): return self.plane.plans[self.plane.active_plan_index]
    @property
    def basic_weight(self): return self.plane.basic_weight
    @property
    def basic_arm(self): return self.plane.basic_arm
    @property
    def cargo_list(self): return self.active_plan.cargo_list
    @property
    def crew_list(self): return self.active_plan.crew_list
    @property
    def fuel_tanks(self): return self.active_plan.fuel_tanks
    @property
    def current_configuration(self): return self.active_plan.configuration

    def subscribe(self, callback): self._observers.append(callback)
    
    def notify(self):
        results = Calculator.calculate_totals(
            self.basic_weight, self.basic_arm, self.crew_list, 
            self.cargo_list, self.fuel_tanks, 
            self.active_plan.configuration
        )
        for callback in self._observers: callback(self, results)

    def set_basic_data(self, w, a): 
        self.plane.basic_weight = float(w); self.plane.basic_arm = float(a); self.notify()
    def update_fuel(self, tank, value): self.fuel_tanks[tank] = float(value); self.notify()
    def set_total_fuel(self, total_lbs): self.active_plan.fuel_tanks = Calculator.distribute_fuel(total_lbs); self.notify()
    def add_crew_member(self, name, weight, ls, count):
        self.crew_list.append(CrewItem(name, weight, ls, "Seat", "free", count=count, fixed=False)); self.notify()
    def remove_crew_member(self, item):
        if item in self.crew_list and not item.fixed: self.crew_list.remove(item); self.notify()
    def update_crew_member(self, item, weight, ls, count):
        item.weight = weight; item.ls = ls; item.count = count; self.notify()
    def add_cargo(self, item: CargoItem): self.cargo_list.append(item); self.notify()
    def remove_cargo(self, item: CargoItem): 
        if item in self.cargo_list: self.cargo_list.remove(item); self.notify()
    def update_cargo_properties(self, item: CargoItem, **kwargs):
        for k, v in kwargs.items(): setattr(item, k, v)
        self.notify()