# core/cargo_constants.py

CARGO_PRESETS = {
    "CDS - BSA":       {"w": 48,  "l": 108, "wt": 0, "desc": "BSA 48x108"},
    "CDS - 48x48":     {"w": 48,  "l": 48,  "wt": 0, "desc": "Standard CDS"},
    "CDS - 52x52":     {"w": 52,  "l": 52,  "wt": 0, "desc": "Large CDS"},
    "Logistic Pallet": {"w": 88,  "l": 104, "wt": 2500, "desc": "463L"},
    "Metric Pallet":   {"w": 108, "l": 0,   "wt": 0,    "desc": "Dynamic 8ft-32ft"},
    "Combatant":       {"w": 20,  "l": 20,  "wt": 250, "desc": "לוחם"},
    "Paratrooper":     {"w": 20,  "l": 20,  "wt": 220, "desc": "צנחן"},
    "Passenger":       {"w": 20,  "l": 20,  "wt": 175, "desc": "נוסע"},
    "General":         {"w": 0,   "l": 0,   "wt": 0,   "desc": "מטען כללי"}
}