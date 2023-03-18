import unittest
from catan.board import Board
from catan.player import Player
from catan.pieces import Settlement
from math import sqrt
from collections import defaultdict

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(50)
        self.player1 = Player("Player 1", "red")
        self.settlement1 = Settlement(0, self.player1)
        self.settlement2 = Settlement(1, self.player1)
        self.settlement3 = Settlement(2, self.player1)
        self.settlement4 = Settlement(3, self.player1)
        self.settlement5 = Settlement(4, self.player1)
        self.settlement6 = Settlement(5, self.player1)


    def tearDown(self):
        del self.board
        del self.player1
        del self.settlement1
        del self.settlement2
        del self.settlement3
        del self.settlement4
        del self.settlement5
        del self.settlement6


    def test_board_initialized_correctly(self):
        self.assertEqual(self.board.hex_radius, 50)
        self.assertAlmostEqual(self.board.hex_height, 50*sqrt(3))
        self.assertIsInstance(self.board._graph, defaultdict)


    def test_add_edge(self):
        self.board.add_edge(self.settlement1, self.settlement2)
        self.assertTrue(self.board.has_edge(self.settlement1, self.settlement2))
        self.assertTrue(self.board.has_edge(self.settlement2, self.settlement1))


    def test_remove_edge(self):
        self.board.add_edge(self.settlement1, self.settlement2)
        self.board.remove_edge(self.settlement1, self.settlement2)
        self.assertFalse(self.board.has_edge(self.settlement1, self.settlement2))
        self.assertFalse(self.board.has_edge(self.settlement1, self.settlement2))


    def test_add_road(self):
        self.assertFalse(self.board.has_road(self.settlement1, self.settlement2))
        self.assertFalse(self.board.has_road(self.settlement2, self.settlement1))
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.assertTrue(self.board.has_road(self.settlement1, self.settlement2))
        self.assertTrue(self.board.has_road(self.settlement2, self.settlement1))


    def test_remove_road(self):
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.board.remove_road(self.settlement1, self.settlement2)
        self.assertFalse(self.board.has_road(self.settlement1, self.settlement2))
        self.assertFalse(self.board.has_road(self.settlement2, self.settlement1))


    def test_has_road(self):
        # make a road of settlements 1 <-> 2 <-> 3 <-> 4
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.board.add_road(self.settlement2, self.settlement3, self.player1)
        self.board.add_road(self.settlement3, self.settlement4, self.player1)
        # check each individual road exists in both orientations
        assert self.board.has_road(self.settlement1, self.settlement2)
        assert self.board.has_road(self.settlement2, self.settlement1)
        assert self.board.has_road(self.settlement2, self.settlement3)
        assert self.board.has_road(self.settlement3, self.settlement2)
        assert self.board.has_road(self.settlement3, self.settlement4)
        assert self.board.has_road(self.settlement4, self.settlement3)
        # check that each settlement is only directly connected with a
        # road to the adjacent settlements, and not ones further down.
        assert not self.board.has_road(self.settlement1, self.settlement3)
        assert not self.board.has_road(self.settlement3, self.settlement1)
        assert not self.board.has_road(self.settlement1, self.settlement4)
        assert not self.board.has_road(self.settlement4, self.settlement1)
        assert not self.board.has_road(self.settlement2, self.settlement4)       
        assert not self.board.has_road(self.settlement4, self.settlement2)
        # check that none of the settlements in the road, have roads
        # connected to the unlinked settlements (settlement 5 and 6).
        assert not self.board.has_road(self.settlement1, self.settlement5)
        assert not self.board.has_road(self.settlement1, self.settlement6)
        assert not self.board.has_road(self.settlement2, self.settlement5)
        assert not self.board.has_road(self.settlement2, self.settlement6)
        assert not self.board.has_road(self.settlement3, self.settlement5)
        assert not self.board.has_road(self.settlement3, self.settlement6)
        assert not self.board.has_road(self.settlement4, self.settlement5)
        assert not self.board.has_road(self.settlement4, self.settlement6)

        # settlement1 = Settlement([0, 0])
        # settlement2 = Settlement([1, 0])
        # player1 = Player("Player 1", "blue")
     
        # self.assertFalse(self.board.has_road(settlement1, settlement2))
        # self.board.add_road(settlement1, settlement2, player1)
        # self.assertTrue(self.board.has_road(settlement1, settlement2))


    def test_get_surrounding_nodes(self):
        
        # Test case needs fixing...
        
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.board.add_road(self.settlement2, self.settlement3, self.player1)
        self.board.add_road(self.settlement3, self.settlement4, self.player1)

        surrounding_nodes = self.board.get_surrounding_nodes(self.settlement1)

        self.assertEqual(len(surrounding_nodes), 3)
        # self.assertTrue((0, 1) in surrounding_nodes)
        # self.assertTrue((1, 0) in surrounding_nodes)
        # self.assertTrue((1, 1) in surrounding_nodes)


    def test_add_settlement(self):
        self.board.add_settlement(self.settlement1, self.player1)
        self.assertIs(self.settlement1.owner, self.player1)


    def test_get_road_owner(self):
        self.board.add_settlement(self.settlement1, self.player1)
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.assertEqual(self.board.get_road_owner(self.settlement1, self.settlement2), self.player1)    


    def test_get_surrounding_nodes(self):
        self.board.add_edge((0, 0), (0, 1))
        self.board.add_edge((0, 0), (1, 0))
        self.assertEqual(self.board.get_surrounding_nodes((0, 0)), [(0, 1), (1, 0)])
        self.assertEqual(self.board.get_surrounding_nodes((0, 1)), [(0, 0)])
        self.assertEqual(self.board.get_surrounding_nodes((1, 0)), [(0, 0)])


    def test_make_random(self):
        b = Board.make_random()
        self.assertEqual(len(b.settlements), 54)
        self.assertEqual(len(b.terrain_tiles), 19)
        del b
    

    def test_settlement_and_terrain_connections(self):
        for terrain_tile in self.board.terrain_tiles.values():
            surrounding_settlements = self.board.get_surrounding_nodes(terrain_tile)
            self.assertEqual(len(surrounding_settlements), 6)
            for settlement in surrounding_settlements:
                self.assertIn(terrain_tile, self.board.get_surrounding_nodes(settlement))
       

if __name__ == "__main__":
    unittest.main()
