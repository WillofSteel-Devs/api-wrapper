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

from .types import Player, Alliance

BASE = "https://api.wos.itsneil.tech"

class Wrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "API-Key": self.api_key,
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
            # raise NotInAlliance() # custom errors still left to do
            raise KeyError
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
            return False # TODO: add better error management
            
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
            return False # TODO: add better error management
            
    def request(self, method: Literal["GET", "POST"], route: str, headers: dict):
        headers = {
            "User-Agent": "Will of Steel API Wrapper",
            "API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        url = BASE + route

        if method not in ["GET", "POST"]:
            return KeyError("Invalid Method")

        response = requests.request(method, url, headers=headers)
        response.status = response.status_code
        return response
