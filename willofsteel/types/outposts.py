from __future__ import annotations
from typing import NamedTuple

class Outpost(NamedTuple):
    profile_id: str
    name: str

    @staticmethod
    def from_data(data: dict) -> Outpost:
        return Outpost(
            profile_id=data["profile_id"],
            name=data["name"]
        )