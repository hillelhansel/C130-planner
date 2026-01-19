# app/config.py

# נתוני C130J-30
LEMAC = 687.4
MAC_LEN = 164.5

# ערכי כיול סופיים
LS_START = 85
LS_END = 1205

# Basic Data
DEFAULT_BASIC_WEIGHT = 91000.0
DEFAULT_BASIC_ARM = 723.0

# קיבולות (זוגות - הוכפלו ב-2)
# AUX: 5810 * 2 = 11620
# EXT: 8900 * 2 = 17800
# IN: 7660 * 2 = 15320
# OUT: 8310 * 2 = 16620
FUEL_CAPACITIES = {
    "Inboard": 15320.0,
    "Outboard": 16620.0,
    "Auxiliary": 11620.0,
    "External": 17800.0
}

# טבלת מומנטים (מעודכנת לטווחים)
FUEL_TABLE_DATA = {
    "Auxiliary": [(0, 0), (1000, 762), (5000, 3789), (10000, 7569), (13000, 9840)],
    "Inboard": [(0, 0), (1000, 760), (5000, 3781), (10000, 7553), (15548, 11739)],
    "Outboard": [(0, 0), (1000, 750), (5000, 3737), (10000, 7461), (16880, 12579)],
    "External": [(0, 0), (1000, 752), (5000, 3759), (10000, 7513), (18184, 13659)]
}

# צבעים - החזרתי טקסט ללבן
COLORS = {
    "Pax": "#00BFFF", "Crew": "#00BFFF", "Pallet": "#FFA500",
    "Metric": "#FFD700", "Drop": "#32CD32", "Gen": "#9370DB",
    "Select": "white", "Error": "red", "Text": "white", "Lines": "white"
}

COMPARTMENT_DEFS = [
    ("C", 345, 383), ("D", 383, 472), ("E", 472, 562), ("F", 562, 652),
    ("G", 652, 742), ("H", 742, 832), ("I", 832, 922), ("J", 922, 1011), 
    ("K", 1011, 1042), ("L", 1042, 1124), ("M", 1124, 1141)
]

LOAD_STATIONS = list(range(357, 1018, 20)) + [1042, 1124, 1141]

# קטלוג מטענים (דוגמה)
CATALOG_ITEMS = {
    "Jeep Hummer": {"weight": 5500, "length": 180, "width": 86, "type": "Gen"},
    "Engine C130": {"weight": 3200, "length": 90, "width": 40, "type": "Metric"},
    "Water Tank": {"weight": 2000, "length": 60, "width": 60, "type": "Pallet"}
}