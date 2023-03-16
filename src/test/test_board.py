import sys; sys.path.append("..");
from catan.pieces import Settlement
import unittest
from catan.player import Player
from catan.board import Board
from math import sqrt
from collections import defaultdict

class TestBoard(unittest.TestCase):
    

    def test_board_initialized_correctly(self):
        board = Board(10)
        self.assertEqual(board.hex_radius, 10)
        self.assertAlmostEqual(board.hex_height, 10*sqrt(3))
        self.assertIsInstance(board._graph, defaultdict)
        
    def setUp(self):
         # Set up a new board with a hex radius of 50 for each test
        self.board = Board(50)

    def test_add_settlement(self):
        player = Player("Player 1", "blue")
        settlement = Settlement([0, 0])
        self.board.add_settlement(settlement, player)
        self.assertEqual(player.num_settlements, 1)
        self.assertIs(settlement.owner, player)  

    def test_get_road_owner(self):
        settlement1 = Settlement([0,0])
        settlement2 = Settlement([1,0])
        player1 = Player("Player 1","blue")

        self.board.add_settlement(settlement1, player1)
        self.board.add_road(settlement1, settlement2, player1)
        self.assertEqual(self.board.get_road_owner(settlement1, settlement2), player1)    

      
    def test_add_road(self):
        settlement1 = Settlement((0,0))
        settlement2 = Settlement((1,0))
        player1 = Player("Player 1","blue")

        self.board.add_settlement(settlement1, player1)
        self.assertFalse(self.board.has_road(settlement1, settlement2))
        self.board.add_road(settlement1, settlement2, player1)
        self.assertTrue(self.board.has_road(settlement1, settlement2))
    
    def test_has_road(self):
        settlement1 = Settlement([0, 0])
        settlement2 = Settlement([1, 0])
        player1 = Player("Player 1", "blue")
     
        self.assertFalse(self.board.has_road(settlement1, settlement2))
        self.board.add_road(settlement1, settlement2, player1)
        self.assertTrue(self.board.has_road(settlement1, settlement2))


    def test_has_road(self):
        self.settlement1 = Settlement([0,0])
        self.settlement2 = Settlement([1,0])
        self.player1 = Player("Player 1","blue")
        self.player2 = Player("Player 2", "red")

        self.board.add_settlement(self.settlement1, self.player1)
        self.board.add_settlement(self.settlement2, self.player2)
        self.assertFalse(self.board.has_road(self.settlement1, self.settlement2))
        self.board.add_road(self.settlement1, self.settlement2, self.player1)
        self.assertTrue(self.board.has_road(self.settlement1, self.settlement2))    

    def test_add_edge(self):
        self.board.add_edge((0, 0), (0, 1))
        self.assertEqual(self.board._graph[(0, 0)], [(0, 1)])
        self.assertEqual(self.board._graph[(0, 1)], [(0, 0)])

    def test_remove_edge(self):
        self.board.add_edge((0, 0), (0, 1))
        self.board.remove_edge((0, 0), (0, 1))
        self.assertEqual(self.board._graph[(0, 0)], [])
        self.assertEqual(self.board._graph[(0, 1)], [])

    def test_has_edge(self):
        self.board.add_edge((0, 0), (0, 1))
        self.assertTrue(self.board.has_edge((0, 0), (0, 1)))
        self.assertTrue(self.board.has_edge((0, 1), (0, 0)))
        self.assertFalse(self.board.has_edge((0, 0), (1, 0)))

    

    def test_get_surrounding_nodes(self):
        self.board.add_edge((0, 0), (0, 1))
        self.board.add_edge((0, 0), (1, 0))
        self.assertEqual(self.board.get_surrounding_nodes((0, 0)), [(0, 1), (1, 0)])
        self.assertEqual(self.board.get_surrounding_nodes((0, 1)), [(0, 0)])
        self.assertEqual(self.board.get_surrounding_nodes((1, 0)), [(0, 0)])


       ###------------------ make_random ---------------####
    def setUp(self):
        self.board = Board.make_random()

    def test_settlement_count(self):
        self.assertEqual(len(self.board.settlements), 54)
    
    def test_terrain_tile_count(self):
        self.assertEqual(len(self.board.terrain_tiles), 19)
    

    def test_settlement_and_terrain_connections(self):
        for terrain_tile in self.board.terrain_tiles.values():
            surrounding_settlements = self.board.get_surrounding_nodes(terrain_tile)
            self.assertEqual(len(surrounding_settlements), 6)
            for settlement in surrounding_settlements:
                self.assertIn(terrain_tile, self.board.get_surrounding_nodes(settlement))
       

        

if __name__ == "__main__":
    unittest.main()
    
