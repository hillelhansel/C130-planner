import json
import os
from app import config
from app.models import AircraftData, ConfigItem, UpdateItem

DATA_FILE = "planner_data.json"
TAIL_NUMBERS = ["661", "662", "663", "665", "667", "668", "669"]

# === רשימת פריטים מלאה (לא מקוצרת) ===
DEFAULT_CONFIG_ITEMS = [
    {"category": "מושבים/אלונקות", "name": "מושב זוגי", "weight_per_unit": 9.0, "full_qty": 60, "qty_in_plane": 60, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "מושב בודד", "weight_per_unit": 5.3, "full_qty": 8, "qty_in_plane": 8, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "עמוד שדרה מרכזי", "weight_per_unit": 30.5, "full_qty": 13, "qty_in_plane": 13, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "תומכי שדרה עליונים ותחתונים", "weight_per_unit": 311.0, "full_qty": 1, "qty_in_plane": 1, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "סופיות שדרה מרכזית", "weight_per_unit": 2.0, "full_qty": 2, "qty_in_plane": 2, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "חלקים 29/32", "weight_per_unit": 1.25, "full_qty": 16, "qty_in_plane": 16, "ls": 620.0},
    {"category": "מושבים/אלונקות", "name": "סולם מילוט", "weight_per_unit": 70.0, "full_qty": 1, "qty_in_plane": 1, "ls": 681.0},
    {"category": "מושבים/אלונקות", "name": "תומך עליון בית גלגל", "weight_per_unit": 5.0, "full_qty": 2, "qty_in_plane": 2, "ls": 740.0},
    {"category": "אמצעי קישרה", "name": "שרשרת 10K", "weight_per_unit": 7.0, "full_qty": 34, "qty_in_plane": 34, "ls": 1040.0},
    {"category": "אמצעי קישרה", "name": "שרשרת 25K", "weight_per_unit": 20.0, "full_qty": 14, "qty_in_plane": 14, "ls": 1100.0},
    {"category": "אמצעי קישרה", "name": "נועל 10K", "weight_per_unit": 3.4, "full_qty": 34, "qty_in_plane": 34, "ls": 743.0},
    {"category": "אמצעי קישרה", "name": "נועל 25K", "weight_per_unit": 6.3, "full_qty": 14, "qty_in_plane": 14, "ls": 1060.0},
    {"category": "אמצעי קישרה", "name": "רצועת 5K", "weight_per_unit": 3.4, "full_qty": 60, "qty_in_plane": 60, "ls": 743.0},
    {"category": "אמצעי קישרה", "name": "טבעות 25K", "weight_per_unit": 2.5, "full_qty": 14, "qty_in_plane": 14, "ls": 1200.0},
    {"category": "אמצעי קישרה", "name": "רצועת 10K", "weight_per_unit": 4.0, "full_qty": 8, "qty_in_plane": 8, "ls": 1200.0},
    {"category": "צב\"ה", "name": "מצנח", "weight_per_unit": 16.5, "full_qty": 1, "qty_in_plane": 1, "ls": 400.0},
    {"category": "צב\"ה", "name": "ח\"א 5", "weight_per_unit": 8.8, "full_qty": 3, "qty_in_plane": 3, "ls": 400.0},
    {"category": "צב\"ה", "name": "רתמת משלח", "weight_per_unit": 8.8, "full_qty": 3, "qty_in_plane": 3, "ls": 350.0},
    {"category": "צב\"ה", "name": "תיק להשלמת ציוד לסירות", "weight_per_unit": 25.0, "full_qty": 2, "qty_in_plane": 2, "ls": 400.0},
    {"category": "צב\"ה", "name": "סירות כנפיים", "weight_per_unit": 95.0, "full_qty": 3, "qty_in_plane": 3, "ls": 400.0},
    {"category": "ציוד כללי", "name": "כננת RETRIEVER", "weight_per_unit": 41.5, "full_qty": 2, "qty_in_plane": 2, "ls": 345.0},
    {"category": "ציוד כללי", "name": "כבל סטטי+תוף", "weight_per_unit": 23.0, "full_qty": 4, "qty_in_plane": 4, "ls": 1171.0},
    {"category": "ציוד כללי", "name": "PRY BAR", "weight_per_unit": 49.0, "full_qty": 2, "qty_in_plane": 2, "ls": 345.0},
    {"category": "ציוד כללי", "name": "תומך זנב", "weight_per_unit": 65.0, "full_qty": 1, "qty_in_plane": 1, "ls": 360.0},
    {"category": "ציוד כללי", "name": "רמפות עזר מרכב", "weight_per_unit": 50.0, "full_qty": 2, "qty_in_plane": 2, "ls": 1060.0},
    {"category": "ציוד כללי", "name": "רמפות עזר מקרקע", "weight_per_unit": 42.0, "full_qty": 2, "qty_in_plane": 2, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "DR", "weight_per_unit": 1320.0, "full_qty": 1, "qty_in_plane": 1, "ls": 743.0},
    {"category": "ציוד כללי", "name": "מוט שחרור נועלים קצר", "weight_per_unit": 4.0, "full_qty": 1, "qty_in_plane": 1, "ls": 500.0},
    {"category": "ציוד כללי", "name": "מוט שחרור נועלים ארוך", "weight_per_unit": 7.0, "full_qty": 1, "qty_in_plane": 1, "ls": 500.0},
    {"category": "ציוד כללי", "name": "מוט הצלת צנחן", "weight_per_unit": 6.0, "full_qty": 1, "qty_in_plane": 1, "ls": 817.0},
    {"category": "ציוד כללי", "name": "מושב ד\"צ", "weight_per_unit": 5.5, "full_qty": 1, "qty_in_plane": 1, "ls": 917.0},
    {"category": "ציוד כללי", "name": "נועל רמפה צהוב", "weight_per_unit": 9.0, "full_qty": 1, "qty_in_plane": 1, "ls": 1041.0},
    {"category": "ציוד כללי", "name": "זרוע W", "weight_per_unit": 8.5, "full_qty": 2, "qty_in_plane": 2, "ls": 937.0},
    {"category": "ציוד כללי", "name": "גלגלת שינוי כיוון", "weight_per_unit": 8.0, "full_qty": 2, "qty_in_plane": 2, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "מיכל מים מלא", "weight_per_unit": 26.3, "full_qty": 2, "qty_in_plane": 2, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "מיכל מים ריק", "weight_per_unit": 9.4, "full_qty": 8, "qty_in_plane": 8, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "רצועת אלונקה + תופסנים", "weight_per_unit": 3.3, "full_qty": 46, "qty_in_plane": 46, "ls": 681.0},
    {"category": "ציוד כללי", "name": "תומך זרוע W", "weight_per_unit": 4.25, "full_qty": 4, "qty_in_plane": 4, "ls": 1030.0},
    {"category": "ציוד כללי", "name": "מחשב DSDTS + תושבת", "weight_per_unit": 25.0, "full_qty": 1, "qty_in_plane": 1, "ls": 743.0},
    {"category": "ציוד כללי", "name": "גלגלת עזר CDS", "weight_per_unit": 4.5, "full_qty": 4, "qty_in_plane": 4, "ls": 1017.0},
    {"category": "ציוד כללי", "name": "תומכי ג'קים", "weight_per_unit": 2.5, "full_qty": 4, "qty_in_plane": 4, "ls": 345.0},
    {"category": "ציוד כללי", "name": "עמודי אלונקות ד\"צ", "weight_per_unit": 15.0, "full_qty": 2, "qty_in_plane": 2, "ls": 897.0},
    {"category": "ציוד כללי", "name": "מוט משיכת כננת", "weight_per_unit": 11.0, "full_qty": 1, "qty_in_plane": 1, "ls": 345.0},
    {"category": "ציוד כללי", "name": "PLCU", "weight_per_unit": 5.0, "full_qty": 10, "qty_in_plane": 10, "ls": 743.0},
    {"category": "ציוד כללי", "name": "ערכת עמדת אלונקות רוחבית", "weight_per_unit": 3.0, "full_qty": 6, "qty_in_plane": 6, "ls": 470.0},
    {"category": "ציוד כללי", "name": "מוט ניקוזים", "weight_per_unit": 10.0, "full_qty": 1, "qty_in_plane": 1, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "כיסוי מנועים", "weight_per_unit": 10.0, "full_qty": 1, "qty_in_plane": 1, "ls": 345.0},
    {"category": "ציוד כללי", "name": "שורינגים קצרים", "weight_per_unit": 15.0, "full_qty": 2, "qty_in_plane": 2, "ls": 360.0},
    {"category": "ציוד כללי", "name": "פחיות שמן הידראולי", "weight_per_unit": 53.0, "full_qty": 1, "qty_in_plane": 1, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "פחיות שמן מנוע", "weight_per_unit": 53.0, "full_qty": 1, "qty_in_plane": 1, "ls": 1200.0},
    {"category": "ציוד כללי", "name": "ספרות מטוס", "weight_per_unit": 20.0, "full_qty": 1, "qty_in_plane": 1, "ls": 339.0},
    {"category": "ציוד כללי", "name": "סולם גפ\"ט", "weight_per_unit": 43.0, "full_qty": 1, "qty_in_plane": 1, "ls": 360.0}
]

def get_default_data():
    fleet_data = {}
    for tail in TAIL_NUMBERS:
        fleet_data[tail] = {
            "weighing": {"weight": 92300.0, "arm": 723.46, "moment": 66775.8},
            "header": {"index": 1, "date": "", "updater": "", "nature": ""},
            "config": DEFAULT_CONFIG_ITEMS,
            "updates": []
        }
    return {
        "catalog": config.CATALOG_ITEMS,
        "fleet": fleet_data
    }

class DataManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.data = cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "fleet" not in data: data["fleet"] = get_default_data()["fleet"]
                    if "catalog" not in data: data["catalog"] = config.CATALOG_ITEMS
                    return data
            except: return get_default_data()
        return get_default_data()

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_fleet_keys(self): 
        return TAIL_NUMBERS

    def get_component_names(self):
        return sorted(list(set([item["name"] for item in DEFAULT_CONFIG_ITEMS])))
        
    def get_catalog(self):
        return self.data.get("catalog", [])

    def get_aircraft_data(self, tail):
        raw = self.data["fleet"].get(tail, {})
        if not raw: 
            self.data["fleet"][tail] = get_default_data()["fleet"]["661"]
            self.save_data()
            raw = self.data["fleet"][tail]
        
        from app.models import AircraftData, ConfigItem, UpdateItem
        
        w = raw.get("weighing", {})
        h = raw.get("header", {})
        
        # המרת מילונים לאובייקטים
        # שימוש ברשימה המלאה והמעודכנת מהקובץ או מברירת המחדל אם חסר
        raw_config = raw.get("config", [])
        if not raw_config:
             # אם זה מטוס חדש שנוצר עכשיו, תן לו את רשימת ברירת המחדל המלאה
             raw_config = DEFAULT_CONFIG_ITEMS

        c_items = [ConfigItem(**i) for i in raw_config]
        u_items = [UpdateItem(
            date=i["date"], adjuster=i["adjuster"], description=i["description"],
            weight_change=i["weight"], arm_change=i["arm"], moment_change=i["moment"]
        ) for i in raw.get("updates", [])]
        
        return AircraftData(
            tail_number=tail,
            weighing_weight=w.get("weight", 92300.0),
            weighing_arm=w.get("arm", 723.46),
            weighing_moment=w.get("moment", 66775.8),
            current_update_index=h.get("index", 1),
            last_update_date=h.get("date", ""),
            last_updater_name=h.get("updater", ""),
            update_nature=h.get("nature", ""),
            config_items=c_items,
            update_items=u_items
        )

    def save_aircraft_data(self, obj):
        tail = obj.tail_number
        config_list = [{"category": c.category, "name": c.name, "weight_per_unit": c.weight_per_unit, "full_qty": c.full_qty, "qty_in_plane": c.qty_in_plane, "ls": c.ls} for c in obj.config_items]
        update_list = [{"date": u.date, "adjuster": u.adjuster, "description": u.description, "weight": u.weight_change, "arm": u.arm_change, "moment": u.moment_change} for u in obj.update_items]
        
        self.data["fleet"][tail] = {
            "weighing": {"weight": obj.weighing_weight, "arm": obj.weighing_arm, "moment": obj.weighing_moment},
            "header": {
                "index": obj.current_update_index,
                "date": obj.last_update_date,
                "updater": obj.last_updater_name,
                "nature": obj.update_nature
            },
            "config": config_list,
            "updates": update_list
        }
        self.save_data()