from dataclasses import dataclass, field
from typing import List, Dict
from app import config

# --- מחלקות נתונים (Data Classes) ---
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
    """מחלקת מצב לשמירת תכנון (לג) ספציפי"""
    name: str
    fuel: float = 0.0
    crew: List[CrewMember] = field(default_factory=list)
    payload: List[CargoItem] = field(default_factory=list)

# --- מחשבון עזר (Static Calculator) ---
class Calculator:
    @staticmethod
    def distribute_fuel(total_fuel):
        """מחלק את הדלק בין המכלים לפי סדר מילוי"""
        tanks = {k: 0.0 for k in config.FUEL_CAPACITIES}
        remaining = total_fuel
        
        # סדר מילוי: חיצוני -> אוקזילרי -> חיצוני (Outboard) -> פנימי (Inboard)
        # שים לב: זהו סדר מילוי בסיסי. במציאות יש לוגיקה מורכבת יותר למטוס C-130J
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
        """מחשב מומנט לדלק לפי טבלאות (אינטרפולציה לינארית)"""
        table = config.FUEL_TABLE_DATA.get(tank_name, [])
        if not table: return 0
        
        for i in range(len(table) - 1):
            w1, m1 = table[i]
            w2, m2 = table[i+1]
            if w1 <= weight <= w2:
                if w2 == w1: return m1
                ratio = (weight - w1) / (w2 - w1)
                return m1 + ratio * (m2 - m1)
        
        # אם חורג מהטבלה - קח את הערך האחרון (או 0 ליתר ביטחון)
        if weight >= table[-1][0]:
            return table[-1][1]
        return 0

# --- הלוגיקה הראשית (Main Logic) ---
class MissionLogic:
    def __init__(self, basic_weight, basic_moment):
        self.basic_weight = basic_weight
        self.basic_moment = basic_moment
        
        self.fuel = 0.0
        self.crew: List[CrewMember] = []
        self.payload: List[CargoItem] = []

    def load_state(self, plan: PlanState):
        """טוען מצב מתוך אובייקט PlanState"""
        self.fuel = plan.fuel
        # העתקה עמוקה כדי למנוע שינויים בטעות בתוכניות אחרות
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
        """מבצע את חישוב המשקלים והאיזון הסופי"""
        
        # 1. Basic Weight (מגיע מניהול הצי)
        total_w = self.basic_weight
        total_m = self.basic_moment
        
        # 2. Crew
        for c in self.crew:
            w_tot = c.weight * c.count
            total_w += w_tot
            total_m += (w_tot * c.ls)
            
        op_w = total_w # Operating Weight
        
        # 3. Payload
        for item in self.payload:
            total_w += item.weight
            total_m += item.moment
            
        zfw = total_w # Zero Fuel Weight
        
        # 4. Fuel
        tanks = Calculator.distribute_fuel(self.fuel)
        fuel_w = sum(tanks.values())
        fuel_m = 0
        for t, w in tanks.items():
            # המומנט בטבלאות הוא לרוב מחולק ב-1000, אז נכפיל חזרה
            # (בהנחה ש-config.FUEL_TABLE_DATA מכיל ערכי אינדקס)
            fuel_m += Calculator.get_fuel_moment(t, w) * 1000
            
        gw = zfw + fuel_w # Gross Weight
        tm = total_m + fuel_m # Total Moment
        
        # חישוב מרכז כובד (CG)
        cg = tm / gw if gw > 0 else 0
        
        # חישוב %MAC
        # הנוסחה: (CG - LEMAC) / MAC_LEN * 100
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