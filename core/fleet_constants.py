# core/fleet_constants.py

LEMAC = 687.4
MAC_LEN = 164.5
LS_START = 85
LS_END = 1205

DEFAULT_BASIC_WEIGHT = 91000.0
DEFAULT_BASIC_ARM = 723.0

FUEL_CAPACITIES = {
    "External": 17800.0, "Auxiliary": 11620.0,
    "Outboard": 16620.0, "Inboard": 15320.0
}

FUEL_TABLE_DATA = {
    "Auxiliary": [(0, 0), (1000, 762), (5000, 3789), (10000, 7569), (13000, 9840)],
    "Inboard": [(0, 0), (1000, 760), (5000, 3781), (10000, 7553), (15548, 11739)],
    "Outboard": [(0, 0), (1000, 750), (5000, 3737), (10000, 7461), (16880, 12579)],
    "External": [(0, 0), (1000, 752), (5000, 3759), (10000, 7513), (18184, 13659)]
}

COMPARTMENT_DEFS = [
    ("C", 345, 383), ("D", 383, 472), ("E", 472, 562), ("F", 562, 652),
    ("G", 652, 742), ("H", 742, 832), ("I", 832, 922), ("J", 922, 1011),
    ("K", 1011, 1042), ("L", 1042, 1124), ("M", 1124, 1141)
]

# הרשימה המלאה שלך
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