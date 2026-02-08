from core.fleet_constants import FUEL_CAPACITIES, FUEL_TABLE_DATA, LEMAC, MAC_LEN

class CalculationService:
    @staticmethod
    def distribute_fuel(total_fuel):
        tanks = {k: 0.0 for k in FUEL_CAPACITIES}
        remaining = total_fuel
        fill_order = ["External", "Auxiliary", "Outboard", "Inboard"]
        
        for name in fill_order:
            if name in FUEL_CAPACITIES:
                cap = FUEL_CAPACITIES[name]
                fill = min(remaining, cap)
                tanks[name] = fill
                remaining -= fill
        return tanks

    @staticmethod
    def get_fuel_moment(tank_name, weight):
        table = FUEL_TABLE_DATA.get(tank_name, [])
        if not table: return 0
        for i in range(len(table) - 1):
            w1, m1 = table[i]
            w2, m2 = table[i+1]
            if w1 <= weight <= w2:
                if w2 == w1: return m1
                ratio = (weight - w1) / (w2 - w1)
                return m1 + ratio * (m2 - m1)
        if weight >= table[-1][0]: return table[-1][1]
        return 0

    @staticmethod
    def calculate_mac(cg):
        return ((cg - LEMAC) / MAC_LEN) * 100