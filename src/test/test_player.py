import unittest

from catan.board import Board
from catan.player import Player
from catan.pieces import Settlement


class TestBoard(unittest.TestCase):

    def setUp(self):
        # create board, players, and settlements
        pass


    def tearDown(self):
        # delete board, players, and settlements
        pass


    def test_settlement_counter(self):
        # ensure counter increments by 1 after placing settlement
        pass


    def test_city_counter(self):
        # ensure counter increments by 1 after placing city
        pass


    def test_road_counter(self):
        # ensure counter increments by 1 after placing road
        pass


    def test_settlement_resource_requirement(self):
        # player must have the required resources to build a settlement
        pass


    def test_city_resource_requirement(self):
        # player must have the required resources to build a city
        pass


    def test_road_resource_requirement(self):
        # player must have the required resources to build a road
        pass


    def test_city_upgrading_settlement(self):
        # city can not be placed, must be upgraded via a settlement
        pass


    def test_settlement_count_limit(self):
        # player has maximum of 5 settlements
        pass


    def test_road_count_limit(self):
        # player has maximum of 15 roads
        pass


    def test_city_count_limit(self):
        # player has maximum of 4 cities
        pass


if __name__ == "__main__":
    unittest.main()
