# app/logic.py
from app import config

class Calculator:
    @staticmethod
    def distribute_fuel(total_fuel):
        tanks = {k: 0.0 for k in config.FUEL_CAPACITIES}
        remaining = total_fuel
        
        # סדר מילוי (לוגיקה פשוטה)
        for name in ["External", "Auxiliary", "Outboard", "Inboard"]:
            cap = config.FUEL_CAPACITIES[name]
            fill = min(remaining, cap)
            tanks[name] = fill
            remaining -= fill
        return tanks

    @staticmethod
    def get_fuel_moment(tank_name, weight):
        table = config.FUEL_TABLE_DATA.get(tank_name, [])
        if not table: return 0
        for i in range(len(table) - 1):
            w1, m1 = table[i]
            w2, m2 = table[i+1]
            if w1 <= weight <= w2:
                ratio = (weight - w1) / (w2 - w1) if (w2 - w1) != 0 else 0
                return m1 + ratio * (m2 - m1)
        return table[-1][1]

    @staticmethod
    def calculate_totals(basic_w, basic_arm, crew_list, cargo_list, fuel_tanks, config_list):
        # 1. Basic Weight
        total_w = basic_w
        total_m = basic_w * basic_arm
        
        # 2. Configuration Items (Shaver/Giluach) - תוספת חדשה
        for item in config_list:
            total_w += item.total_weight
            total_m += item.moment
            
        # 3. Crew
        for c in crew_list:
            w_tot = c.weight * c.count
            total_w += w_tot
            total_m += (w_tot * c.ls)
            
        op_w = total_w  # Operating Weight
        
        # 4. Cargo
        for item in cargo_list:
            total_w += item.weight
            total_m += item.moment
            
        zfw = total_w
        
        # 5. Fuel
        fuel_w = sum(fuel_tanks.values())
        fuel_m = 0
        for t, w in fuel_tanks.items():
            fuel_m += Calculator.get_fuel_moment(t, w) * 1000
            
        gw = zfw + fuel_w
        tm = total_m + fuel_m
        
        cg = tm / gw if gw > 0 else 0
        mac = ((cg - config.LEMAC) / config.MAC_LEN) * 100
        
        return {
            "basic_w": basic_w,
            "op_w": op_w,
            "zfw": zfw,
            "fuel_w": fuel_w,
            "gw": gw,
            "cg": cg,
            "mac": mac
        }