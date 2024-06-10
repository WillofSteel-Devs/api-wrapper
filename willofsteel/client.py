"""
WillofSteel API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~

A wrapper for the Will of Steel API

:copyright: (C) 2024-present ItsNeil
:license: MIT, see LICENSE for more details

"""
from __future__ import annotations
from typing import Literal
import requests
import logging

from .types import Player, Alliance, MarketOrder, UnitType, ItemType, LoggingObject, convert_str_to_IT, convert_str_to_UT, Outpost
from .constants import BASE, ALL_ITEMS, MISSING
from .utils import parse_error, setup_logging
from .exceptions import *

class Client:
    def __init__(self, api_key: str, logger: LoggingObject = MISSING):
        self.api_key = api_key
        self.headers = {
            "API-Key": self.api_key,
            "User-Agent": "Will of Steel API Wrapper",
            "Accept": "application/json",
            "X-API-Version": "0.3"
        }

        setup_logging(logger if logger else LoggingObject())
        self._verify_key()

    def _verify_key(self) -> None:
        response = self.request("GET", "/verify", self.headers)
        if response.status == 403:
            raise InvalidKey
        elif response.status == 200:
            logging.info("Key verification successful.")
        else:
            raise ServerError

    def get_player(self) -> Player:
        """
        Retrieve player information.
        
        """
        response = self.request("GET", "/player", self.headers)    
        # There can not be a 403 error raised as we already verified the key.
        if response.status == 200:
            data = response.json()
            logging.debug(f"Got player data successfully: {data}. Returning with converting to Model.")
            return Player.from_response(data)

    def get_player_inventory(self) -> dict[ItemType, int]:
        """
        Retrieve player inventory.

        """
        response = self.request("GET", "/inventory", self.headers)
        if response.status == 200:
            data = response.json()
            logging.debug(f"Got player inventory data successfully: {data}. Returning with converting to Model.")
            return {convert_str_to_IT(item_id): amount for item_id, amount in data["items"].items()}
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def get_player_army(self) -> dict[UnitType, int]:
        """
        Retrieve player army.
        
        """
        response = self.request("GET", "/army", self.headers)
        if response.status == 200:
            data = response.json()
            logging.debug(f"Got player army data successfully: {data}. Returning with converting to Model.")
            return {convert_str_to_UT(unit_type): amount for unit_type, amount in data["units"].items()}
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def get_outposts(self) -> list[Outpost]:
        """
        Retrieve all outposts.
        
        """
        response = self.request("GET", "/outposts", self.headers)
        if response.status == 200:
            data = response.json()
            logging.debug(f"Got outposts data successfully: {data}. Returning with converting to Model.")
            return [Outpost.from_data(outpost) for outpost in data["outposts"]]
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def get_alliance(self) -> dict:
        """
        Retrieve alliance information.

        Returns
        -------
        Optional[:class:`~willofsteel.types.Alliance`]
        
        """
        response = self.request("GET", "/alliance", headers=self.headers)
        status = response.status
        if status == 400:
            raise NotInAlliance
        data = response.json()
        logging.debug(f"Got alliance data successfully: {data}. Returning with converting to Model.")
        return Alliance.from_response(data)

    def update_alliance_name(self, new_name: str) -> bool:
        """
        Update the name of the alliance.

        Parameters
        ----------
        new_name: :class:`str`
            The new name of the alliance.

        Returns
        -------
        :class:`bool`
        
        """
        if len(new_name) > 32: # this is not an official limit. just a wrapper limit for now
            raise LimitExceeded(32, "name")
        headers = self.headers
        headers["update_type"] = "name"
        headers["new_name"] = new_name
        response = self.request("POST", "/alliance", headers=headers)
        status = response.status
        if status == 200:
            logging.debug("Alliance name update was successful. Resp code: 200")
            return True
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def update_alliance_user_limit(self, new_limit: str) -> bool:
        """
        Update the user limit of the alliance.

        Parameters
        ----------
        new_limit: :class:`str`
            The new user limit of the alliance.

        Returns
        -------
        :class:`bool`
        
        """
        if new_limit > 50:
            return KeyError # return an error which says it cant be more than 50 
        headers = self.headers
        headers["update_type"] = "limit"
        headers["new_limit"] = new_limit
        response = self.request("POST", "/alliance", headers=headers)        
        status = response.status
        if status == 200:
            logging.debug("Alliance user limit update was successful. Resp code: 200")
            return True
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def get_all_offers(self, offer_type: Literal["buy", "sell"]) -> list[MarketOrder]:
        """
        Retrieve all offers.

        Parameters
        ----------
        offer_type: :class:`Literal["buy", "sell"]`
            The type of offer to retrieve.
        
        """
        if offer_type not in ["buy", "sell"]:
            raise KeyError("Invalid offer type")
        offers = []
        params = {
            "order_type": offer_type,
        }
        for item_id in ALL_ITEMS:
            params["item_type"] = item_id
            response = self.request("GET", "/market", headers=self.headers, params=params)
            json_data = response.json()
            if response != 200:
                parse_error(json_data["detail"])
            logging.debug(f"Got offer data for {item_id}: {str(json_data)}")
            number_of_orders = len(json_data["orders"])
            if number_of_orders == 0:
                continue
            for order_uuid, order_data in json_data["orders"].items():
                offers.append(MarketOrder.from_response(order_uuid, order_data))
        return offers

    def get_offer(self, offer_type: Literal["buy", "sell"], item_id: str) -> list[MarketOrder]:
        """
        Retrieve an offer.

        Parameters
        ----------
        offer_type: :class:`Literal["buy", "sell"]`
            The type of offer to retrieve.
        item_id: :class:`str`
            The ID of the item to retrieve offers for.
        
        """
        if offer_type not in ["buy", "sell"]:
            raise InvalidInput("offer_type")
        offers = []
        params = {
            "order_type": offer_type,
            "item_type": item_id
        }
        response = self.request("GET", "/market", headers=self.headers, params=params)
        json_data = response.json()
        logging.debug(f"Got offer data for {item_id}: {str(json_data)}")
        if response.status_code != 200:
            parse_error(json_data["detail"])
        for order_uuid, order_data in json_data["orders"].items():
            offers.append(MarketOrder.from_response(order_uuid, order_data))
        return offers

    def recruit_troop(self, unit_type: UnitType, amount: int, currency: Literal["gold", "silver"] = "gold") -> bool:
        """
        Recruit troops.

        Parameters
        ----------
        unit_type: :class:`~willofsteel.types.UnitType`
            The type of unit to recruit.
        amount: :class:`int`
            The amount of units to recruit.
        currency: :class:`str`
            The currency to use for recruitment. Defaults to gold.
            
        Returns
        -------
        :class:`bool`
        
        """
        new_troop_name = unit_type.name.lower().replace(" ", "_").replace("'", "")
        query_params = {
            "troop": new_troop_name,
            "amount": amount,
            "currency": currency
        }
        response = self.request("POST", "/recruit", self.headers, query_params)
        status = response.status
        if status == 200:
            logging.debug("Troop recruitment was successful. Resp code: 200")
            return True
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def request(self, method: Literal["GET", "POST"], route: str, headers: dict, params: dict = None):
        url = BASE + route

        if method not in ["GET", "POST"]:
            return KeyError("Invalid Method")

        response = requests.request(method, url, headers=headers, params=params)
        response.status = response.status_code
        if response.status == 500:
            raise ServerError
        return response
