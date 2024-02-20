BASE = "https://api.willofsteel.me"
ALL_ITEMS = ["IRON_FRAME", "BAKERY_TOKEN", "FARMHOUSE_TOKEN", "STOREHOUSE_TOKEN", "MORALE_TOKEN", "HEALING_TOKEN", "LUCKYCHARM_TOKEN", "LOOT_TOKEN", "BAKERY_FRAME", "FARMHOUSE_FRAME", "STOREHOUSE_FRAME", "MORALE_FRAME", "HEALING_FRAME", "LUCKYCHARM_FRAME", "LOOT_FRAME"]

class _MissingObject:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False
    
    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'
    
MISSING = _MissingObject()