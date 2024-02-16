from enum import Enum
from typing import NamedTuple

class UnitProperties(NamedTuple):
    name: str
    attack: int
    defense: int


class UnitType(UnitProperties, Enum):
    INFANTRY = UnitProperties("Infantry", 30, 20)
    CAVALRY = UnitProperties("Cavalry", 50, 30)
    ARTILLERY = UnitProperties("Artillery", 90, 30)
    ASSASSINS = UnitProperties("Assassins", 150, 25)
    BOWMEN = UnitProperties("Bowmen", 10, 35)
    BIG_BOWMEN = UnitProperties("Big Bowmen", 15, 55)
    HEAVY_MEN = UnitProperties("Heavy Men", 15, 85)
    KINGS_GUARDS = UnitProperties("King's Guards", 30, 155)