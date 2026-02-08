import json
import os
from core.fleet_constants import DEFAULT_CONFIG_ITEMS
from core.models import AircraftData, ConfigItem, UpdateItem

DATA_FILE = "planner_data.json"

class DataService:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.data_cache = None

    def load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.data_cache = json.load(f)
            except:
                self.data_cache = self._create_default_data()
        else:
            self.data_cache = self._create_default_data()
            self.save_data()
        return self.data_cache

    def save_data(self):
        if self.data_cache:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data_cache, f, indent=4, ensure_ascii=False)

    def get_catalog(self):
        # החזרת הקטלוג מתוך הקובץ או ברירת המחדל
        data = self.load_data()
        return data.get("catalog", DEFAULT_CONFIG_ITEMS)

    def get_aircraft(self, tail_number):
        data = self.load_data()
        if "fleet" not in data: data["fleet"] = {}
        
        if tail_number not in data["fleet"]:
            data["fleet"][tail_number] = self._get_default_aircraft_dict()
            self.save_data()

        raw = data["fleet"][tail_number]
        
        # טעינת קונפיגורציה עם הגנה מקריסה
        raw_config = raw.get("config", [])
        if not raw_config:
             # אם אין קונפיגורציה למטוס, טוענים את הדיפולט
             config_list = [ConfigItem(**i) for i in DEFAULT_CONFIG_ITEMS]
        else:
            try:
                config_list = [ConfigItem(**i) for i in raw_config]
            except TypeError:
                config_list = [ConfigItem(**i) for i in DEFAULT_CONFIG_ITEMS]

        update_list = [UpdateItem(**i) for i in raw.get("updates", [])]
        
        return AircraftData(
            tail_number=tail_number,
            weighing_weight=raw["weighing"].get("weight", 92300.0),
            weighing_arm=raw["weighing"].get("arm", 723.46),
            weighing_moment=raw["weighing"].get("moment", 66775.8),
            current_update_index=raw["header"].get("index", 1),
            last_update_date=raw["header"].get("date", ""),
            last_updater_name=raw["header"].get("updater", ""),
            update_nature=raw["header"].get("nature", ""),
            config_items=config_list,
            update_items=update_list
        )

    def save_aircraft(self, aircraft: AircraftData):
        if not self.data_cache: self.load_data()
        
        ac_dict = {
            "weighing": {
                "weight": aircraft.weighing_weight,
                "arm": aircraft.weighing_arm,
                "moment": aircraft.weighing_moment
            },
            "header": {
                "index": aircraft.current_update_index,
                "date": aircraft.last_update_date,
                "updater": aircraft.last_updater_name,
                "nature": aircraft.update_nature
            },
            "config": [item.to_dict() for item in aircraft.config_items],
            "updates": [item.to_dict() for item in aircraft.update_items]
        }
        
        self.data_cache["fleet"][aircraft.tail_number] = ac_dict
        self.save_data()

    def _create_default_data(self):
        return {"catalog": DEFAULT_CONFIG_ITEMS, "fleet": {}}

    def _get_default_aircraft_dict(self):
        return {
            "weighing": {"weight": 92300.0, "arm": 723.46, "moment": 66775.8},
            "header": {"index": 1, "date": "", "updater": "", "nature": ""},
            "config": [item for item in DEFAULT_CONFIG_ITEMS],
            "updates": []
        }