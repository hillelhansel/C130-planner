import json
import os
from core.models import AircraftData, ConfigItem, UpdateItem
from services.catalog_service import CatalogService

FLEET_FILE = "planner_data.json"

class FleetService:
    def __init__(self):
        self.catalog = CatalogService()
        self.cache = self._load()

    def _load(self):
        if os.path.exists(FLEET_FILE):
            try:
                with open(FLEET_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "fleet" not in data: data["fleet"] = {}
                    if "updates_catalog" not in data: data["updates_catalog"] = []
                    return data
            except: pass
        return {"fleet": {}, "updates_catalog": []}

    def save(self):
        with open(FLEET_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=4, ensure_ascii=False)

    def get_all_tail_numbers(self):
        return ["661", "662", "663", "665", "667", "668", "669"]

    def get_aircraft(self, tail):
        if tail not in self.cache["fleet"]:
            self.cache["fleet"][tail] = self._create_default()
            # לא שומרים לדיסק עד שהמשתמש לוחץ שמור
            
        raw = self.cache["fleet"][tail]
        
        raw_conf = raw.get("config", [])
        if not raw_conf:
            conf = [ConfigItem(**i) for i in self.catalog.get_default_config()]
        else:
            conf = [ConfigItem(**i) for i in raw_conf]

        return AircraftData(
            tail_number=tail,
            weighing_weight=raw["weighing"].get("weight", 92000.0),
            weighing_arm=raw["weighing"].get("arm", 700.0),
            weighing_moment=raw["weighing"].get("moment", 64400.0),
            current_update_index=raw["header"].get("index", 1),
            last_update_date=raw["header"].get("date", ""),
            last_updater_name=raw["header"].get("updater", ""),
            update_nature=raw["header"].get("nature", ""),
            config_items=conf,
            update_items=[UpdateItem(**i) for i in raw.get("updates", [])]
        )

    def _serialize_aircraft(self, ac: AircraftData):
        return {
            "weighing": {"weight": ac.weighing_weight, "arm": ac.weighing_arm, "moment": ac.weighing_moment},
            "header": {"index": ac.current_update_index, "date": ac.last_update_date, "updater": ac.last_updater_name, "nature": ac.update_nature},
            "config": [item.to_dict() for item in ac.config_items],
            "updates": [item.to_dict() for item in ac.update_items]
        }

    def update_cache_only(self, ac: AircraftData):
        """שומר לזיכרון בלבד (למעבר בין מטוסים)"""
        self.cache["fleet"][ac.tail_number] = self._serialize_aircraft(ac)

    def save_aircraft(self, ac: AircraftData):
        """שומר לזיכרון וגם לקובץ (לחיצה על שמור)"""
        self.update_cache_only(ac)
        self.save()

    def get_updates_catalog(self):
        return self.cache.get("updates_catalog", [])

    def add_to_updates_catalog(self, name, weight, arm):
        for item in self.cache["updates_catalog"]:
            if item["name"] == name: return
        self.cache["updates_catalog"].append({"name": name, "weight": weight, "arm": arm})
        self.save()

    def _create_default(self):
        return {
            "weighing": {"weight": 92000.0, "arm": 700.0, "moment": 64400.0},
            "header": {"index": 1},
            "config": self.catalog.get_default_config(),
            "updates": []
        }