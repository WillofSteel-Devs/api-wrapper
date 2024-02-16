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
import asyncio
import atexit

from .types import Player, Alliance, MarketOrder
from .constants import BASE, ALL_ITEMS
from .utils import parse_error
from .exceptions import *

class Wrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "API-Key": self.api_key,
            "User-Agent": "Will of Steel API Wrapper",
            "Content-Type": "application/json"
        }      
        # self._verify_key() # not implemented in API as of now

    def _verify_key(self) -> None:
        raise NotImplementedError("Key Verification not available.")

    def get_player(self) -> dict:
        response = self.request("GET", "/player", self.headers)    
        # There can not be a 403 error raised as we already verified the key.
        if response.status == 200:
            data = response.json()
            return Player.from_response(data)

    def get_alliance(self) -> dict:
        response = self.request("GET", "/alliance", headers=self.headers)
        status = response.status
        if status == 400:
            raise NotInAlliance
        data = response.json()
        return Alliance.from_response(data)

    def update_alliance_name(self, new_name: str) -> bool:
        if len(new_name) > 32: # this is not an official limit. just a wrapper limit for now
            return KeyError # return an error which says it cant be more than 32 chars 
        headers = self.headers
        headers["update_type"] = "name"
        headers["new_name"] = new_name
        response = self.request("POST", "/alliance", headers=headers)
        status = response.status
        if status == 200:
            return True
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    def update_alliance_user_limit(self, new_limit: str) -> bool:
        if new_limit > 50:
            return KeyError # return an error which says it cant be more than 50 
        headers = self.headers
        headers["update_type"] = "limit"
        headers["new_limit"] = new_limit
        response = self.request("POST", "/alliance", headers=headers)        
        status = response.status
        if status == 200:
            return True
        else:
            json = response.json()
            parse_error(json["detail"])
            print(json["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")
            
    def get_all_offers(self, offer_type: Literal["buy", "sell"]):
        if offer_type not in ["buy", "sell"]:
            raise KeyError("Invalid offer type")
        offers = []
        params = {
            "order_type": offer_type,
        }
        for item_id in ALL_ITEMS:
            print(item_id)
            params["item_type"] = item_id
            response = self.request("GET", "/market", headers=self.headers, params=params)
            json_data = response.json()
            if response != 200:
                parse_error(json_data["detail"])
            number_of_orders = len(json_data["orders"])
            if number_of_orders == 0:
                continue
            for order_uuid, order_data in json_data["orders"].items():
                offers.append(MarketOrder.from_response(order_uuid, order_data))
        return offers

    def get_offer(self, offer_type: Literal["buy", "sell"], item_id: str):
        if offer_type not in ["buy", "sell"]:
            raise InvalidInput("offer_type")
        offers = []
        params = {
            "order_type": offer_type,
            "item_type": item_id
        }
        response = self.request("GET", "/market", headers=self.headers, params=params)
        json_data = response.json()
        if response != 200:
            parse_error(json_data["detail"])
        for order_uuid, order_data in json_data["orders"].items():
            offers.append(MarketOrder.from_response(order_uuid, order_data))
        return offers

    def request(self, method: Literal["GET", "POST"], route: str, headers: dict, params: dict = None):
        url = BASE + route

        if method not in ["GET", "POST"]:
            return KeyError("Invalid Method")

        response = requests.request(method, url, headers=headers, params=params)
        response.status = response.status_code
        if response.status == 500:
            raise ServerError
        return response