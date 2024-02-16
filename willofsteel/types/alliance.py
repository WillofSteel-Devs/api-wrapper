from datetime import datetime
from typing import NamedTuple


class Alliance(NamedTuple):
    owner: int
    created_at: datetime
    name: str
    user_limit: int
    bank: int

    @staticmethod
    def from_response(data: dict):
        if data is None:
            return None
        
        return Alliance(
            owner = data["owner"],
            created_at=data["created_at"],
            name=data["name"],
            user_limit=data["user_limit"],
            bank=data["bank"]
        )