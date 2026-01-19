# app/models.py
from dataclasses import dataclass, field
from typing import List, Dict

# --- Fleet & Excel Models ---

@dataclass
class ConfigItem:
    category: str
    name: str
    weight_per_unit: float
    full_qty: int          
    qty_in_plane: int      
    ls: float              
    
    @property
    def weight(self): return self.weight_per_unit
    
    @property
    def qty(self): return self.qty_in_plane
    @qty.setter
    def qty(self, value): self.qty_in_plane = value
    
    @property
    def max_qty(self): return self.full_qty

    @property
    def qty_removed(self): return self.full_qty - self.qty_in_plane
    @property
    def weight_removed(self): return self.qty_removed * self.weight_per_unit
    
    @property
    def total_weight(self): return self.qty_in_plane * self.weight_per_unit
    @property
    def moment(self): return (self.total_weight * self.ls)
    @property
    def moment_removed(self): return (self.weight_removed * self.ls) / 1000.0

@dataclass
class UpdateItem:
    date: str
    adjuster: str
    description: str
    weight_change: float
    arm_change: float
    moment_change: float

@dataclass
class AircraftData:
    tail_number: str
    # נתוני שקילה
    weighing_weight: float = 92300.0
    weighing_arm: float = 723.46
    weighing_moment: float = 66775.8
    
    # נתוני כותרת עדכון (Header Info)
    current_update_index: int = 1
    last_update_date: str = ""
    last_updater_name: str = ""
    update_nature: str = ""

    config_items: List[ConfigItem] = field(default_factory=list)
    update_items: List[UpdateItem] = field(default_factory=list)

    @property
    def total_removed_weight(self): return sum(item.weight_removed for item in self.config_items)
    @property
    def total_removed_moment(self): return sum(item.moment_removed for item in self.config_items)
    @property
    def total_updates_weight(self): return sum(item.weight_change for item in self.update_items)
    @property
    def total_updates_moment(self): return sum(item.moment_change for item in self.update_items)

    @property
    def basic_weight(self):
        return self.weighing_weight - self.total_removed_weight + self.total_updates_weight

    @property
    def basic_moment_raw(self):
        return (self.weighing_moment * 1000) - (self.total_removed_moment * 1000) + (self.total_updates_moment * 1000)
    
    @property
    def basic_arm_calc(self):
        if self.basic_weight == 0: return 0
        return self.basic_moment_raw / self.basic_weight

# --- Planner Models (תאימות) ---
@dataclass
class CargoItem:
    name: str; weight: float; ls: float; length: float; width: float; item_type: str 
    side: str = "Center"; y_offset: float = 0.0
    @property
    def moment(self): return self.weight * self.ls

@dataclass
class CrewItem:
    name: str; weight: float; ls: float; type: str; pos: str; count: int = 1; fixed: bool = True

@dataclass
class PlanState:
    name: str
    cargo_list: List[CargoItem] = field(default_factory=list)
    crew_list: List[CrewItem] = field(default_factory=list)
    fuel_tanks: Dict[str, float] = field(default_factory=dict)
    configuration: List[ConfigItem] = field(default_factory=list) 

@dataclass
class PlaneState:
    tail_number: str; basic_weight: float; basic_arm: float
    base_configuration: List[ConfigItem] = field(default_factory=list)
    plans: List[PlanState] = field(default_factory=list)
    active_plan_index: int = 0