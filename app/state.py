from app.data import DataManager
from app.logic import MissionLogic, PlanState
# ייבוא למקרה שצריך ליצור אובייקטים חדשים
from core.models import CargoItem, CrewMember 

class MissionStateManager:
    def __init__(self, tail_number="661"):
        self.db = DataManager()
        self.tail_number = tail_number
        self.observers = []
        
        # טעינת נתונים
        aircraft_data = self.db.get_aircraft_data(tail_number)
        basic_weight = aircraft_data.basic_weight
        basic_moment = aircraft_data.basic_moment_raw 
        
        self.logic = MissionLogic(basic_weight, basic_moment)
        
        self.plans = [PlanState("Plan A")]
        self.active_plan_index = 0
        
        # אתחול אנשי צוות ברירת מחדל (LM וכו') אם הרשימה ריקה
        if not self.plans[0].crew:
             # דוגמה לאתחול בסיסי - ניתן לשנות את המשקלים/מיקומים
             lm = CrewMember("LM", 200, 200, 1, fixed=True) 
             self.logic.crew.append(lm)
             self.plans[0].crew.append(lm)

    @property
    def active_plan(self):
        return self.plans[self.active_plan_index]

    # --- התיקון הקריטי: חשיפת הרשימות לתצוגה ---
    @property
    def crew_list(self):
        return self.logic.crew

    @property
    def cargo_list(self):
        return self.logic.payload
    # ------------------------------------------

    def get_plan_names(self):
        return [p.name for p in self.plans]

    def set_active_plan(self, index):
        if 0 <= index < len(self.plans):
            self.active_plan_index = index
            self.logic.load_state(self.active_plan)
            self.notify()

    def add_plan(self, name):
        new_plan = PlanState(name)
        new_plan.fuel = self.logic.fuel
        # העתקה עמוקה כדי למנוע צימוד בין תוכניות
        new_plan.crew = [CrewMember(c.name, c.weight, c.station, c.count, c.fixed) for c in self.logic.crew]
        new_plan.payload = [
            CargoItem(p.name, p.weight, p.station, p.length, p.width, p.type_code, p.ref_point, p.ls, p.y_offset) 
            for p in self.logic.payload
        ]
        self.plans.append(new_plan)
        self.set_active_plan(len(self.plans) - 1)

    def rename_active_plan(self, new_name):
        self.active_plan.name = new_name
        self.notify()

    def update_fuel(self, weight):
        self.logic.set_fuel(weight)
        self.active_plan.fuel = weight
        self.notify()

    # --- עדכון פונקציות צוות (תמיכה ב-UI) ---
    def add_crew_member(self, name, weight, station, count=1):
        self.logic.add_crew(name, weight, station, count)
        # עדכון ה-Plan הפעיל
        self.active_plan.crew = list(self.logic.crew)
        self.notify()

    def update_crew_member(self, item, weight, station, count):
        # מכיוון שזה אובייקט, השינוי בלוגיקה משתקף מיד, אבל צריך לעדכן את ה-Plan
        item.weight = weight
        item.station = station
        item.count = count
        self.notify()

    def remove_crew_member(self, item):
        if item in self.logic.crew:
            self.logic.crew.remove(item)
            self.active_plan.crew = list(self.logic.crew)
            self.notify()
            
    def remove_crew(self, idx): # תמיכה בקריאה לפי אינדקס (מהמניפסט)
        self.logic.remove_crew(idx)
        self.active_plan.crew = list(self.logic.crew)
        self.notify()

    # --- עדכון פונקציות מטען ---
    def add_cargo(self, item):
        self.logic.add_payload(item)
        self.active_plan.payload = list(self.logic.payload)
        self.notify()

    def remove_cargo(self, item):
        if item in self.logic.payload:
            self.logic.payload.remove(item)
            self.active_plan.payload = list(self.logic.payload)
            self.notify()

    def remove_payload(self, idx): # תמיכה בקריאה לפי אינדקס (מהמניפסט)
        self.logic.remove_payload(idx)
        self.active_plan.payload = list(self.logic.payload)
        self.notify()

    def subscribe(self, callback):
        self.observers.append(callback)

    def notify(self):
        data = self.logic.calculate_totals()
        for callback in self.observers:
            callback(self, data)