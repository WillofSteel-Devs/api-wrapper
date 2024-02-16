from typing import NamedTuple

class MarketOrder(NamedTuple):
    uuid: str
    item_id: str
    order_type: str
    price: int
    amount: int

    @staticmethod
    def from_response(uuid: str, data: dict):

        return MarketOrder(
            uuid=uuid,
            item_id=data["item_type"],
            order_type=data["order_type"],
            price=data["price"],
            amount=data["amount"],
        )