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
        
    def test_add_edge(self):
        board = Board(50)
        board.add_edge((0, 0), (0, 1))
        self.assertTrue(board.has_edge((0, 0), (0, 1)))
        self.assertTrue(board.has_edge((0, 1), (0, 0)))

    def test_remove_edge(self):
        board = Board(50)
        board.add_edge((0, 0), (0, 1))
        board.remove_edge((0, 0), (0, 1))
        self.assertFalse(board.has_edge((0, 0), (0, 1)))
        self.assertFalse(board.has_edge((0, 1), (0, 0)))

    def test_add_road(self):
        board = Board(50)
        board.add_road((0, 0), (0, 1))
        self.assertTrue(board.has_road((0, 0), (0, 1)))
        self.assertTrue(board.has_road((0, 1), (0, 0)))

    def test_remove_road(self):
        board = Board(50)
        board.add_road((0, 0), (0, 1))
        board.remove_road((0, 0), (0, 1))
        self.assertFalse(board.has_road((0, 0), (0, 1)))
        self.assertFalse(board.has_road((0, 1), (0, 0)))

    def test_get_surrounding_nodes(self):
        board = Board(50)
        board.add_edge((0, 0), (0, 1))
        board.add_edge((0, 0), (1, 0))
        board.add_edge((0, 0), (1, 1))
        surrounding_nodes = board.get_surrounding_nodes((0, 0))
        self.assertEqual(len(surrounding_nodes), 3)
        self.assertTrue((0, 1) in surrounding_nodes)
        self.assertTrue((1, 0) in surrounding_nodes)
        self.assertTrue((1, 1) in surrounding_nodes)
        
    def test_has_road():
     board = Board(50)
     board.add_road((0, 0), (1, 0))
     board.add_road((0, 0), (0, 1))
     board.add_road((1, 0), (1, 1))

    assert board.has_road((0, 0), (1, 0))
    assert board.has_road((1, 0), (0, 0))
    assert board.has_road((0, 0), (0, 1))
    assert board.has_road((0, 1), (0, 0))
    assert board.has_road((1, 0), (1, 1))
    assert board.has_road((1, 1), (1, 0))

    assert not board.has_road((0, 0), (0, -1))
    assert not board.has_road((0, 0), (1, 1))
    assert not board.has_road((1, 1), (0, 1))
    assert not board.has_road((0, 1), (1, 1))

        

if __name__ == "__main__":
    unittest.main()
    
