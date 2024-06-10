from typing import NamedTuple
from enum import Enum

class ItemProperties(NamedTuple):
    item_id: str
    name: str

class ItemType(ItemProperties, Enum):
    IRON_FRAME = ItemProperties("IRON_FRAME", "Iron Frame")


    BAKERY_TOKEN = ItemProperties("BAKERY_TOKEN", "Bakery Token")
    FARMHOUSE_TOKEN = ItemProperties("FARMHOUSE_TOKEN", "FarmHouse Token")
    STOREHOUSE_TOKEN = ItemProperties("STOREHOUSE_TOKEN", "Storehouse Token")
    MORALE_TOKEN = ItemProperties("MORALE_TOKEN", "Morale Token")
    HEALING_TOKEN = ItemProperties("HEALING_TOKEN", "Healing Token")
    LUCKYCHARM_TOKEN = ItemProperties("LUCKYCHARM_TOKEN", "Lucky Charm Token")
    LOOT_TOKEN = ItemProperties("LOOT_TOKEN", "Loot Token")

    BAKERY_FRAME = ItemProperties("BAKERY_FRAME", "Bakery Frame")
    FARMHOUSE_FRAME = ItemProperties("FARMHOUSE_FRAME", "FarmHouse Frame")
    STOREHOUSE_FRAME = ItemProperties("STOREHOUSE_FRAME", "Storehouse Frame")
    MORALE_FRAME = ItemProperties("MORALE_FRAME", "Morale Frame")
    HEALING_FRAME = ItemProperties("HEALING_FRAME", "Healing Frame")
    LUCKYCHARM_FRAME = ItemProperties("LUCKYCHARM_FRAME", "Lucky Charm Frame")
    LOOT_FRAME = ItemProperties("LOOT_FRAME", "Loot Frame")

    MYSTERY_SCROLL = ItemProperties("MYSTERY_SCROLL", "Mystery Scroll")

StringToItemTypeConversion = {
    "IRON_FRAME": ItemType.IRON_FRAME,
    "BAKERY_TOKEN": ItemType.BAKERY_TOKEN,
    "FARMHOUSE_TOKEN": ItemType.FARMHOUSE_TOKEN,
    "STOREHOUSE_TOKEN": ItemType.STOREHOUSE_TOKEN,
    "MORALE_TOKEN": ItemType.MORALE_TOKEN,
    "HEALING_TOKEN": ItemType.HEALING_TOKEN,
    "LUCKYCHARM_TOKEN": ItemType.LUCKYCHARM_TOKEN,
    "LOOT_TOKEN": ItemType.LOOT_TOKEN,
    "BAKERY_FRAME": ItemType.BAKERY_FRAME,
    "FARMHOUSE_FRAME": ItemType.FARMHOUSE_FRAME,
    "STOREHOUSE_FRAME": ItemType.STOREHOUSE_FRAME,
    "MORALE_FRAME": ItemType.MORALE_FRAME,
    "HEALING_FRAME": ItemType.HEALING_FRAME,
    "LUCKYCHARM_FRAME": ItemType.LUCKYCHARM_FRAME,
    "LOOT_FRAME": ItemType.LOOT_FRAME,
    "MYSTERY_SCROLL": ItemType.MYSTERY_SCROLL
}

def convert_str_to_IT(item_str: str) -> ItemType:
    return StringToItemTypeConversion[item_str]