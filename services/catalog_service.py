from core.fleet_constants import DEFAULT_CONFIG_ITEMS
from core.cargo_constants import CARGO_PRESETS

class CatalogService:
    def get_presets(self):
        return CARGO_PRESETS

    def get_default_config(self):
        # מחזיר עותק חדש כדי למנוע דריסה
        return [item.copy() for item in DEFAULT_CONFIG_ITEMS]