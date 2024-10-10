import unittest
import logging
import asyncio
from unittest.mock import AsyncMock, patch
import unittest.async_case
import willofsteel
from willofsteel.async_client import AsyncClient
from willofsteel.exceptions import *
from willofsteel.types import *


class TestAsyncClient(unittest.async_case.IsolatedAsyncioTestCase):

    def setUp(self):
        patcher = patch(
            'willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
        self.addCleanup(patcher.stop)
        self.mock_request = patcher.start()
        self.mock_request.return_value = {'success': True,
                                          'user_id': 707274479751135243}, 200
        self.client = AsyncClient(
            'valid_key', logger=LoggingObject(level=logging.CRITICAL))

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_validate_key_valid_key_raises_no_exception(self, mock_get):
        mock_get.return_value = {'success': True,
                                 'user_id': 707274479751135243}, 200
        try:
            await self.client._verify_key()
            self.assertTrue(True)
        except InvalidKey:
            self.fail("InvalidKey exception raised unexpectedly")

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_validate_key_invalid_key_raises_InvalidKey_exception(self, mock_get):
        mock_get.return_value = {'detail': 'Not authenticated'}, 403
        with self.assertRaises(willofsteel.exceptions.InvalidKey):
            await self.client._verify_key()

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_player_returns_player_object(self, mock_get):
        mock_get.return_value = {
            "user_id": 0,
            "registered_at": "2019-08-24T14:15:22Z",
            "gold": 0,
            "ruby": 0,
            "silver": 0,
            "units": {
                "property1": 0,
                "property2": 0
            },
            "npc_level": 0,
            "last_npc_win": "2019-08-24T14:15:22Z",
            "votes": 0,
            "queue_slots": 0,
            "observer": True,
            "peace": 0,
            "letter_bird": 0,
            "food_stored": 0,
            "prestige": 0,
            "alliance": {
                "owner": 0,
                "created_at": "2019-08-24T14:15:22Z",
                "name": "string",
                "user_limit": 0,
                "bank": 0
            }
        }, 200
        response = await self.client.get_player()
        self.assertIsInstance(response, Player)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_player_inventory_returns_dictionary_of_items(self, mock_get):
        mock_get.return_value = {
            "items": {"BAKERY_TOKEN": 10, "HEALING_TOKEN": 1}}, 200
        response = await self.client.get_player_inventory()
        self.assertIsInstance(response, dict)
        for item in response.values():
            self.assertIsInstance(item, int)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_player_army_returns_dictionary_of_units(self, mock_get):
        mock_get.return_value = {
            "units": {"infantry": 500, "cavalry": 100, "artillery": 50}}, 200
        response = await self.client.get_player_army()
        self.assertIsInstance(response, dict)
        for unit in response.values():
            self.assertIsInstance(unit, int)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_outposts_returns_list_of_outpost_objects(self, mock_get):
        mock_get.return_value = {'outposts': [{'profile_id': 'abc', 'name': 'an_outpost'}, {
            'profile_id': 'xyz', 'name': 'another_outpost'}]}, 200
        response = await self.client.get_outposts()
        self.assertIsInstance(response, list)
        for outpost in response:
            self.assertIsInstance(outpost, Outpost)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_alliance_in_alliance_returns_alliance_object(self, mock_get):
        mock_get.return_value = {'owner': 1,
                                 'created_at': '2023-01-01 01:-1:01',
                                 'name': 'Alliance',
                                 'user_limit': 50,
                                 'bank': 1}, 200
        response = await self.client.get_alliance()
        self.assertIsInstance(response, Alliance)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_alliance_not_in_alliance_raises_NotInAlliance_Exception(self, mock_get):
        mock_get.return_value = {"success": False,
                                 "detail": "alliance not found"}, 400
        try:
            await self.client.get_alliance()
            self.fail("NotInAlliance exception not raised")
        except NotInAlliance:
            self.assertTrue(True)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_update_alliance_name_valid_name_returns_True(self, mock_get):
        mock_get.return_value = {"updated": "name",
                                 "old": "old name", "new": "new name"}, 200
        response = await self.client.update_alliance_name('New Name')
        self.assertTrue(response)
        response = await self.client.update_alliance_name('a'*32)
        self.assertTrue(response)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_update_alliance_name_invalid_name_raises_LimitExceeded_Exception(self, mock_get):
        mock_get.return_value = {'detail': 'Limit exceeded'}, 400
        with self.assertRaises(LimitExceeded):
            await self.client.update_alliance_name('a'*33)

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_all_offers_valid_offer_type_returns_list_of_offer_objects(self, mock_get):
        mock_get.return_value = {'orders': {'1': {
            'item_type': 'LUCKYCHARM_TOKEN', 'order_type': 'buy', 'price': 1, 'amount': 1}}}, 200
        response = await self.client.get_all_offers('buy')
        self.assertIsInstance(response, list)
        for offer in response:
            self.assertIsInstance(offer, MarketOrder
                                  )
        response = await self.client.get_all_offers('sell')
        self.assertIsInstance(response, list)
        for offer in response:
            self.assertIsInstance(offer, MarketOrder
                                  )

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_all_offers_invalid_offer_type_raises_KeyError_Exception(self, mock_get):
        mock_get.return_value = {'success': False,
                                 'detail': 'invalid order type'}, 400
        with self.assertRaises(KeyError):
            await self.client.get_all_offers('invalid_offer_type')

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_offer_valid_offer_type_returns_list_of_offer_objects(self, mock_get):
        mock_get.return_value = {'orders': {'1': {
            'item_type': 'LUCKYCHARM_TOKEN', 'order_type': 'buy', 'price': 1, 'amount': 1}}}, 200
        response = await self.client.get_offer('buy', 'LUCKYCHARM_TOKEN')
        self.assertIsInstance(response, list)
        for offer in response:
            self.assertIsInstance(offer, MarketOrder
                                  )
        response = await self.client.get_offer('sell', 'LUCKYCHARM_TOKEN')
        self.assertIsInstance(response, list)
        for offer in response:
            self.assertIsInstance(offer, MarketOrder
                                  )

    @patch('willofsteel.async_client.AsyncClient.request', new_callable=AsyncMock)
    async def test_get_offer_invalid_offer_type_raises_InvalidInput_Exception(self, mock_get):
        mock_get.return_value = {'success': False,
                                 'detail': 'invalid order type'}, 400
        with self.assertRaises(InvalidInput):
            await self.client.get_offer('invalid_offer_type', 'LUCKYCHARM_TOKEN')
