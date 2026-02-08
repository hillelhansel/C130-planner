
from dataclasses import dataclass, field
from typing import List
from core.models import CrewMember, CargoItem
from services.fleet_service import FleetService
from services.catalog_service import CatalogService
from services.calc_service import CalculationService

@dataclass
class PlanState:
    name: str
    fuel_weight: float = 30000.0
    crew: List[CrewMember] = field(default_factory=list)
    payload: List[CargoItem] = field(default_factory=list)

class MissionManager:
    def __init__(self, tail_number="661"):
        # אתחול ה-Services
        self.fleet_service = FleetService()
        self.catalog_service = CatalogService()
        
        # טעינת המטוס
        self.tail_number = tail_number
        self.aircraft = self.fleet_service.get_aircraft(tail_number)
        
        # אתחול המשימה
        self.plans: List[PlanState] = [PlanState("Leg 1")]
        self.active_index = 0
        self._observers = []
        
        self._init_default_crew()

    # --- גישה לנתונים ---
    @property
    def active_plan(self): return self.plans[self.active_index]
    @property
    def fuel_weight(self): return self.active_plan.fuel_weight
    @property
    def crew(self): return self.active_plan.crew
    @property
    def payload(self): return self.active_plan.payload

    def get_cargo_presets(self):
        # MissionManager מתווך בין ה-UI לבין הקטלוג
        return self.catalog_service.get_presets()

    # --- לוגיקה עסקית ---
    def _init_default_crew(self):
        if not self.active_plan.crew:
            defaults = [("Pilot", 200, 200), ("Co-Pilot", 200, 200), ("Navigator", 200, 200), ("Loadmaster", 200, 245)]
            for n, w, s in defaults: self.active_plan.crew.append(CrewMember(n, w, s, fixed=True))

    def get_plan_names(self): return [p.name for p in self.plans]
    
    def set_active_plan(self, idx): 
        if 0 <= idx < len(self.plans): self.active_index = idx; self.notify()
        
    def add_plan(self, name):
        self.plans.append(PlanState(name, fuel_weight=self.active_plan.fuel_weight))
        self.active_index = len(self.plans) - 1
        self._init_default_crew()
        self.notify()

    def set_fuel(self, w): self.active_plan.fuel_weight = w; self.notify()
    def add_crew(self, n, w, s, c=1): self.active_plan.crew.append(CrewMember(n, w, s, c)); self.notify()
    def remove_crew(self, i): self.active_plan.crew.pop(i); self.notify()
    def update_crew(self, i, n, w, s, c):
        m = self.active_plan.crew[i]; m.name=n; m.weight=w; m.station=s; m.count=c; self.notify()
    
    def add_cargo(self, item): self.active_plan.payload.append(item); self.notify()
    def update_cargo(self, i, item): self.active_plan.payload[i]=item; self.notify()
    def remove_payload(self, i): self.active_plan.payload.pop(i); self.notify()

    def subscribe(self, cb): self._observers.append(cb)
    
    def notify(self):
        res = self.calculate_current_state()
        for cb in self._observers: cb(self, res)

    def calculate_current_state(self):
        # 1. משקל בסיס (מגיע מה-AircraftData שנטען ב-FleetService)
        total_w = self.aircraft.basic_weight
        total_m = self.aircraft.basic_moment_raw
        
        # 2. צוות
        for c in self.active_plan.crew:
            w = c.weight * c.count
            total_w += w
            total_m += (w * c.ls)
        
        # 3. מטען
        for p in self.active_plan.payload:
            total_w += p.weight
            total_m += p.moment
        zfw = total_w
        
        # 4. דלק (חישוב באמצעות CalcService שהוא טהור מתמטיקה)
        tanks = CalculationService.distribute_fuel(self.active_plan.fuel_weight)
        fuel_w = sum(tanks.values())
        fuel_m = 0
        for tank, amount in tanks.items():
            fuel_m += CalculationService.get_fuel_moment(tank, amount) * 1000
            
        gw = zfw + fuel_w
        tm = total_m + fuel_m
        cg = tm / gw if gw > 0 else 0
        
        return {
            "basic_w": self.aircraft.basic_weight,
            "gw": gw, "cg": cg, "mac": CalculationService.calculate_mac(cg), 
            "zfw": zfw, "fuel_w": fuel_w, "tanks": tanks, 
            "plan_name": self.active_plan.name
        }
