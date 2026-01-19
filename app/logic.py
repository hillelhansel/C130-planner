from dataclasses import dataclass, field
from typing import List, Dict
from app import config

# --- מחלקות נתונים ---
@dataclass
class CrewMember:
    name: str
    weight: float
    station: float
    count: int = 1
    
    @property
    def ls(self):
        return self.station

@dataclass
class CargoItem:
    name: str
    weight: float
    station: float
    
    @property
    def moment(self):
        return self.weight * self.station

@dataclass
class PlanState:
    name: str
    fuel: float = 0.0
    crew: List[CrewMember] = field(default_factory=list)
    payload: List[CargoItem] = field(default_factory=list)

# --- מחשבון עזר ---
class Calculator:
    @staticmethod
    def distribute_fuel(total_fuel):
        tanks = {k: 0.0 for k in config.FUEL_CAPACITIES}
        remaining = total_fuel
        fill_order = ["External", "Auxiliary", "Outboard", "Inboard"]
        for name in fill_order:
            if name in config.FUEL_CAPACITIES:
                cap = config.FUEL_CAPACITIES[name]
                fill = min(remaining, cap)
                tanks[name] = fill
                remaining -= fill
        return tanks

    @staticmethod
    def get_fuel_moment(tank_name, weight):
        table = config.FUEL_TABLE_DATA.get(tank_name, [])
        if not table: return 0
        for i in range(len(table) - 1):
            w1, m1 = table[i]
            w2, m2 = table[i+1]
            if w1 <= weight <= w2:
                if w2 == w1: return m1
                ratio = (weight - w1) / (w2 - w1)
                return m1 + ratio * (m2 - m1)
        if weight >= table[-1][0]:
            return table[-1][1]
        return 0

# --- לוגיקה ראשית ---
class MissionLogic:
    def __init__(self, basic_weight, basic_moment):
        self.basic_weight = basic_weight
        self.basic_moment = basic_moment
        self.fuel = 0.0
        self.crew = []
        self.payload = []

    def load_state(self, plan: PlanState):
        self.fuel = plan.fuel
        self.crew = [CrewMember(c.name, c.weight, c.station, c.count) for c in plan.crew]
        self.payload = [CargoItem(p.name, p.weight, p.station) for p in plan.payload]

    def set_fuel(self, weight):
        self.fuel = weight

    def add_crew(self, name, weight, station):
        self.crew.append(CrewMember(name, weight, station))

    def remove_crew(self, idx):
        if 0 <= idx < len(self.crew):
            self.crew.pop(idx)

    def add_payload(self, name, weight, station):
        self.payload.append(CargoItem(name, weight, station))

    def update_payload(self, idx, name, weight, station):
        if 0 <= idx < len(self.payload):
            self.payload[idx] = CargoItem(name, weight, station)

    def remove_payload(self, idx):
        if 0 <= idx < len(self.payload):
            self.payload.pop(idx)

    def calculate_totals(self):
        total_w = self.basic_weight
        total_m = self.basic_moment
        
        for c in self.crew:
            w_tot = c.weight * c.count
            total_w += w_tot
            total_m += (w_tot * c.ls)
            
        op_w = total_w 
        
        for item in self.payload:
            total_w += item.weight
            total_m += item.moment
            
        zfw = total_w 
        
        tanks = Calculator.distribute_fuel(self.fuel)
        fuel_w = sum(tanks.values())
        fuel_m = 0
        for t, w in tanks.items():
            fuel_m += Calculator.get_fuel_moment(t, w) * 1000
            
        gw = zfw + fuel_w 
        tm = total_m + fuel_m 
        cg = tm / gw if gw > 0 else 0
        mac = ((cg - config.LEMAC) / config.MAC_LEN) * 100
        
        return {
            "basic_w": self.basic_weight,
            "op_w": op_w,
            "zfw": zfw,
            "fuel_w": fuel_w,
            "gw": gw,
            "cg": cg,
            "mac": mac,
            "tanks": tanks
        }