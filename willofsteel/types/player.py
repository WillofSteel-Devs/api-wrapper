from typing import NamedTuple
from datetime import datetime
from .troops import UnitType

class Player(NamedTuple):
    id: int
    registered_at: datetime
    gold: int
    ruby: int
    silver: int
    units: dict[UnitType, int]
    npc_level: int
    last_npc_win: datetime | None
    votes: int
    queue_slots: int
    observer: bool
    peace: int
    letter_bird: int
    food_stored: int
    prestige: int

    @staticmethod
    def from_response(data: dict):
        if data is None:
            return None
        return Player(
            id=data["user_id"],
            registered_at=data["registered_at"],
            gold=data.get("gold", 0),
            ruby=data.get("ruby", 0),
            silver=data.get("silver", 0),
            units=data.get("units", {}),
            npc_level=data.get("npc_level", 0),
            last_npc_win=data.get("last_npc_win", None),
            votes=data.get("votes", 0),
            queue_slots=data.get("queue_slots", 0),
            observer=data.get("observer", True),
            peace=data.get("peace", True),
            letter_bird=data.get("letter_bird", True),
            food_stored=data.get("food_stored", 0),
            prestige=data.get("prestige", 0),
        )