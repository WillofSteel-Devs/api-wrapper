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

StringToUnitTypeConversion = {
    "infantry": UnitType.INFANTRY,
    "cavalry": UnitType.CAVALRY,
    "artillery": UnitType.ARTILLERY,
    "assassins": UnitType.ASSASSINS,
    "bowmen": UnitType.BOWMEN,
    "big_bowmen": UnitType.BIG_BOWMEN,
    "heavy_men": UnitType.HEAVY_MEN,
    "kings_guards": UnitType.KINGS_GUARDS
}

def convert_str_to_UT(unit_str: str) -> UnitType:
    return StringToUnitTypeConversion[unit_str]