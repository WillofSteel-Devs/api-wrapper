"""
WillofSteel API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~

Asynchronous wrapper for the Will of Steel API.

:copyright: (C) 2024-present ItsNeil
:license: MIT, see LICENSE for more details

"""
from __future__ import annotations
from typing import Literal
import logging

import aiohttp
import asyncio
import atexit

from .types import Player, Alliance, MarketOrder, UnitType, ItemType, LoggingObject, convert_str_to_IT, convert_str_to_UT, Outpost
from .constants import BASE, ALL_ITEMS, MISSING
from .utils import parse_error, setup_logging
from .exceptions import *


class AsyncClient:
    """
    Asynchronous client for the Will of Steel API.

    Parameters
    ----------
    api_key: :class:`str`
        The API key to use.
    logger: :class:`~willofsteel.types.LoggingObject`
        The logger to use. Defaults to MISSING.
    use_existing_loop: :class:`bool`
        Whether to use an existing event loop. Defaults to False.

    """

    def __init__(self, api_key: str, logger: LoggingObject = MISSING):
        self.api_key = api_key
        self.headers = {
            "API-Key": self.api_key,
            "User-Agent": "Will of Steel API Wrapper",
            "Accept": "application/json",
            "X-API-Version": "0.3"
        }
        self._is_verified = False
        self._user_id = -1
        self._session = None
        setup_logging(logger if logger else LoggingObject())

        event_loop = asyncio.get_event_loop()
        if event_loop.is_running():
            event_loop.create_task(self._async_setup())
        else:
            asyncio.run(self._async_setup())

    @property
    def is_verified(self):
        """
        Whether the API key is verified. This property is not intended to be set.
        """
        return self._is_verified

    @is_verified.setter
    def is_verified(self, value):
        if self._is_verified:
            raise AttributeError("Cannot set is_verified property.")
        elif not isinstance(value, bool):
            raise TypeError("is_verified property must be a boolean.")
        self._is_verified = value

    @property
    def user_id(self):
        """
        The id of the user associated with the api key. This property is not intended to be set.
        """
        if not self._is_verified:
            raise AttributeError(
                "AsyncClient.user_id is not available until its api key is verified.")
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if self._is_verified:
            raise AttributeError("Cannot set user_id property.")
        self._user_id = value

    async def _async_setup(self):
        """
        Setup the asynchronous parts of the client.

        """
        self._session = aiohttp.ClientSession()
        atexit.register(asyncio.run, self._session.close())
        await self._verify_key()

    async def _verify_key(self) -> None:
        data, status = await self.request("GET", "/verify", self.headers)
        if (status == 403) or (not data.get("success")):
            raise InvalidKey
        elif status == 200:
            logging.info("Key verification successful.")
            self._user_id = data["user_id"]
            self._is_verified = True
        else:
            raise ServerError

    async def get_player(self) -> Player:
        """
        Retrieve player information.

        Returns
        -------
        :class:`~willofsteel.types.Player`

        """
        data, status = await self.request("GET", "/player", self.headers)
        # There can not be a 403 error raised as we already verified the key.
        if status == 200:
            logging.debug(
                f"Got player data successfully: {data}. Returning with converting to Model.")
            return Player.from_response(data)

    async def get_player_inventory(self) -> dict[ItemType, int]:
        """
        Retrieve player inventory.

        Returns
        -------
        :class:`dict`[`~willofsteel.types.ItemType`, :class:`int`]

        """
        data, status = await self.request("GET", "/inventory", self.headers)
        if status == 200:
            logging.debug(
                f"Got player inventory data successfully: {data}. Returning with converting to Model.")
            return {convert_str_to_IT(item_id): amount for item_id, amount in data["items"].items()}
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def get_player_army(self) -> dict[UnitType, int]:
        """
        Retrieve player army.

        Returns
        -------
        :class:`dict`[`~willofsteel.types.UnitType`, :class:`int`]

        """
        data, status = await self.request("GET", "/army", self.headers)
        if status == 200:
            logging.debug(
                f"Got player army data successfully: {data}. Returning with converting to Model.")
            return {convert_str_to_UT(unit_type): amount for unit_type, amount in data["units"].items()}
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def get_outposts(self) -> list[Outpost]:
        """
        Retrieve all outposts.

        Returns
        -------
        :class:`list`[`~willofsteel.types.Outpost`]

        """
        data, status = await self.request("GET", "/outpost/list", self.headers)
        if status == 200:
            logging.debug(
                f"Got outposts data successfully: {data}. Returning with converting to Model.")
            return [Outpost.from_data(outpost) for outpost in data["outposts"]]
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def get_alliance(self) -> Alliance:
        """
        Retrieve alliance information.

        Returns
        -------
        :class:`~willofsteel.types.Alliance`

        """
        data, status = await self.request("GET", "/alliance", headers=self.headers)
        if status == 400:
            raise NotInAlliance
        logging.debug(
            f"Got alliance data successfully: {data}. Returning with converting to Model.")
        return Alliance.from_response(data)

    async def update_alliance_name(self, new_name: str) -> bool:
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
        if len(new_name) > 32:  # this is not an official limit. just a wrapper limit for now
            raise LimitExceeded(32, "name")
        headers = self.headers.copy()
        headers["update_type"] = "name"
        headers["new_name"] = new_name
        data, status = await self.request("POST", "/alliance", headers=headers)
        if status == 200:
            logging.debug(
                "Alliance name update was successful. Resp code: 200")
            return True
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def update_alliance_user_limit(self, new_limit: str) -> bool:
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
            return KeyError  # return an error which says it cant be more than 50
        headers = self.headers.copy()
        headers["update_type"] = "limit"
        headers["new_limit"] = new_limit
        data, status = await self.request("POST", "/alliance", headers=headers)
        if status == 200:
            logging.debug(
                "Alliance user limit update was successful. Resp code: 200")
            return True
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def get_all_offers(self, offer_type: Literal["buy", "sell"]) -> list[MarketOrder]:
        """
        Retrieve all offers.

        Parameters
        ----------
        offer_type: :class:`Literal["buy", "sell"]`
            The type of offer to retrieve.

        Returns
        -------
        :class:`list`[`~willofsteel.types.MarketOrder`]

        """
        if offer_type not in ["buy", "sell"]:
            raise KeyError("Invalid offer type")
        offers = []
        params = {
            "order_type": offer_type,
        }
        for item_id in ALL_ITEMS:
            params["item_type"] = item_id
            data, status = await self.request(
                "GET", "/market", headers=self.headers, params=params)
            if status != 200:
                parse_error(data["detail"])
            logging.debug(f"Got offer data for {item_id}: {str(data)}")
            number_of_orders = len(data["orders"])
            if number_of_orders == 0:
                continue
            for order_uuid, order_data in data["orders"].items():
                offers.append(MarketOrder.from_response(
                    order_uuid, order_data))
        return offers

    async def get_offer(self, offer_type: Literal["buy", "sell"], item_id: str) -> list[MarketOrder]:
        """
        Retrieve an offer.

        Parameters
        ----------
        offer_type: :class:`Literal["buy", "sell"]`
            The type of offer to retrieve.
        item_id: :class:`str`
            The ID of the item to retrieve offers for.

        Returns
        -------
        :class:`list`[`~willofsteel.types.MarketOrder`]

        """
        if offer_type not in ["buy", "sell"]:
            raise InvalidInput("offer_type")
        offers = []
        params = {
            "order_type": offer_type,
            "item_type": item_id
        }
        data, status = await self.request(
            "GET", "/market", headers=self.headers, params=params)
        logging.debug(f"Got offer data for {item_id}: {str(data)}")
        if status != 200:
            parse_error(data["detail"])
        for order_uuid, order_data in data["orders"].items():
            offers.append(MarketOrder.from_response(order_uuid, order_data))
        return offers

    async def recruit_troop(self, unit_type: UnitType, amount: int, currency: Literal["gold", "silver"] = "gold") -> bool:
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
        data, status = await self.request("POST", "/recruit", self.headers, query_params)
        if status == 200:
            logging.debug("Troop recruitment was successful. Resp code: 200")
            return True
        else:
            parse_error(data["detail"])
            print(data["detail"])
            print("This error was not automatically detected, please report this to the maintainers (or fix it yourself)!")

    async def request(self, method: Literal["GET", "POST"], route: str, headers: dict, params: dict = None):
        """
        Send an HTTP request and return the response.

        Parameters
        ----------
        method: :class:`str`
            The HTTP method to use.
        route: :class:`str`
            The route to send the request to.
        headers: :class:`dict`
            The headers to send with the request.
        params: :class:`dict`
            The query parameters to send with the request. Defaults to None.

        Returns
        -------
        :class:`dict` The json response from the api,
        :class:`int` The status code of the response

        """
        url = BASE + route

        if method not in ["GET", "POST"]:
            return KeyError("Invalid Method")

        async with self._session.request(method, url, headers=headers, params=params) as response:
            if response.status == 500:
                raise ServerError
            data = await response.json()
            return data, response.status

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self._session.close()
