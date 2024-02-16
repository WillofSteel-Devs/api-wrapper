from .exceptions import *

def parse_error(error: str):
    # Alliance errors
    if error == "invalid update type":
        raise InvalidInput("update_type")
    elif error == "new name not specified":
        raise InvalidInput("new_name")
    elif error == "new limit not specified":
        raise InvalidInput("new_limit")
    elif error == "no alliance found":
        raise NotInAlliance
    elif error == "alliance already exists":
        raise NameAlreadyExists()
    
    # Market errors
    elif error == "invalid order type":
        raise InvalidInput("order_type")
    elif error == "invalid item type":
        raise InvalidInput("item_type")