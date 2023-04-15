import unittest

from catan.models.board import Board
from catan.models.player import Player
from catan.models.settlement import Settlement


class TestBoard(unittest.TestCase):

    def setUp(self):
        # create board, players, and settlements
        pass


    def tearDown(self):
        # delete board, players, and settlements
        pass


    def test_no_adjacent_settlements(self):
        # settlements can not be placed next to adjacent settlements
        pass


    def test_touching_roads(self):
        # roads must be placed touching the players roads or settlements
        pass


    def test_touching_settlements(self):
        # settlements must be placed touching the players roads,
        # excluding the first two settlements placed
        pass


    def test_non_touching_settlements(self):
        # first two settlements can be placed free standing (not
        # touching an existing road)
        pass


if __name__ == "__main__":
    unittest.main()
