from app.data import DataManager
from app.logic import MissionLogic, PlanState

class MissionStateManager:
    def __init__(self, tail_number="661"):
        self.db = DataManager()
        self.tail_number = tail_number
        self.observers = []
        
        # --- התיקון הקריטי ---
        # שליפת נתוני המטוס כ-Object מה-DataManager החדש
        aircraft_data = self.db.get_aircraft_data(tail_number)
        
        # שימוש ב-Properties של המודל לחישוב נכון
        basic_weight = aircraft_data.basic_weight
        basic_moment = aircraft_data.basic_moment_raw # מומנט מלא לחישובים
        
        # אתחול הלוגיקה עם הנתונים האמיתיים
        self.logic = MissionLogic(basic_weight, basic_moment)
        
        self.plans = [PlanState("Plan A")]
        self.active_plan_index = 0

    @property
    def active_plan(self):
        return self.plans[self.active_plan_index]

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
        new_plan.crew = list(self.logic.crew)
        new_plan.payload = list(self.logic.payload)
        self.plans.append(new_plan)
        self.set_active_plan(len(self.plans) - 1)

    def rename_active_plan(self, new_name):
        self.active_plan.name = new_name
        self.notify()

    # Methods delegated to logic
    def update_fuel(self, weight):
        self.logic.set_fuel(weight)
        self.active_plan.fuel = weight
        self.notify()

    def add_crew(self, name, weight, station):
        self.logic.add_crew(name, weight, station)
        self.active_plan.crew = list(self.logic.crew)
        self.notify()

    def remove_crew(self, idx):
        self.logic.remove_crew(idx)
        self.active_plan.crew = list(self.logic.crew)
        self.notify()

    def add_payload(self, name, weight, station):
        self.logic.add_payload(name, weight, station)
        self.active_plan.payload = list(self.logic.payload)
        self.notify()

    def update_payload(self, idx, name, weight, station):
        self.logic.update_payload(idx, name, weight, station)
        self.active_plan.payload = list(self.logic.payload)
        self.notify()

    def remove_payload(self, idx):
        self.logic.remove_payload(idx)
        self.active_plan.payload = list(self.logic.payload)
        self.notify()

    # Observer pattern
    def subscribe(self, callback):
        self.observers.append(callback)

    def notify(self):
        data = self.logic.calculate_totals()
        for callback in self.observers:
            callback(self, data)