import sys; sys.path.append("..");

import unittest
from catan.board import Board
from math import sqrt
from collections import defaultdict

class TestBoard(unittest.TestCase):

    def test_board_initialized_correctly(self):
        board = Board(10)
        self.assertEqual(board.hex_radius, 10)
        self.assertAlmostEqual(board.hex_height, 10*sqrt(3))
        self.assertIsInstance(board._graph, defaultdict)

if __name__ == "__main__":
    unittest.main()