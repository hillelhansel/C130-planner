from dataclasses import dataclass, field
from typing import List

# --- ניהול צי (Fleet) ---
@dataclass
class ConfigItem:
    category: str
    name: str
    weight_per_unit: float
    full_qty: int
    qty_in_plane: int
    ls: float

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
    weighing_weight: float
    weighing_arm: float
    weighing_moment: float
    current_update_index: int
    last_update_date: str
    last_updater_name: str
    update_nature: str
    config_items: List[ConfigItem]
    update_items: List[UpdateItem]

    @property
    def total_removed_weight(self):
        return sum((item.full_qty - item.qty_in_plane) * item.weight_per_unit for item in self.config_items)

    @property
    def total_removed_moment(self):
        m = 0
        for item in self.config_items:
            w_removed = (item.full_qty - item.qty_in_plane) * item.weight_per_unit
            m += (w_removed * item.ls)
        return m / 1000.0

    @property
    def total_updates_weight(self):
        return sum(u.weight_change for u in self.update_items)

    @property
    def total_updates_moment(self):
        return sum(u.moment_change for u in self.update_items)

    @property
    def basic_weight(self):
        return self.weighing_weight - self.total_removed_weight + self.total_updates_weight

    @property
    def basic_moment_raw(self):
        base_m = self.weighing_moment * 1000
        rem_m = self.total_removed_moment * 1000
        upd_m = self.total_updates_moment * 1000
        return base_m - rem_m + upd_m

    @property
    def basic_arm_calc(self):
        if self.basic_weight == 0: return 0
        return self.basic_moment_raw / self.basic_weight

# --- תכנון משימה (Mission) ---
# אלו המחלקות שהיו חסרות וגרמו לקריסה

@dataclass
class CrewMember:
    name: str
    weight: float
    station: float
    count: int = 1
    fixed: bool = False # נדרש עבור פאנל הצוות
    
    @property
    def ls(self):
        return self.station

@dataclass
class CargoItem:
    name: str
    weight: float
    station: float
    # שדות נוספים שנדרשים על ידי cargo.py
    length: float = 0.0
    width: float = 0.0
    type_code: str = "Gen"
    ref_point: str = "Center"
    
    # שדות פנימיים לחישובים ותצוגה
    ls: float = field(default=0.0) 
    y_offset: float = 0.0
    
    @property
    def moment(self):
        return self.weight * self.station