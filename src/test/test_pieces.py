import unittest
from catan.models.board import Board
from catan.models.player import Player
from catan.models.settlement import Settlement
from catan.models.emptysettlement import EmptySettlement

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board.make_random()
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "blue")

    def tearDown(self):
        del self.board
        del self.player1
        del self.player2

    def test_no_adjacent_settlements(self):
        empty_settlement1 = self.board.settlements[3]
        empty_settlement2 = self.board.settlements[4]

        # Place the first settlement for Player 1
        self.board.add_settlement(empty_settlement1, self.player1)

        # Attempt to place a settlement for Player 2 adjacent to Player 1's settlement
        adjacent = False
        for node in self.board.get_surrounding_nodes(empty_settlement1):
            if node == empty_settlement2:
                adjacent = True
                break

        if adjacent:
            with self.assertRaises(Exception):
                self.board.add_settlement(empty_settlement2, self.player2)
        else:
            self.board.add_settlement(empty_settlement2, self.player2)

    def test_touching_roads(self):
        empty_settlement1 = self.board.settlements[3]
        empty_settlement2 = self.board.settlements[8]
        self.board.add_settlement(empty_settlement1, self.player1)
        self.board.add_settlement(empty_settlement2, self.player1)

        self.board.add_road(empty_settlement1, empty_settlement2, self.player1)
        self.assertTrue(self.board.has_road(empty_settlement1, empty_settlement2))

    def test_touching_settlements(self):
        empty_settlement1 = self.board.settlements[3]
        empty_settlement2 = self.board.settlements[8]
        empty_settlement3 = self.board.settlements[14]
        self.board.add_settlement(empty_settlement1, self.player1)
        self.board.add_settlement(empty_settlement2, self.player1)
        self.board.add_road(empty_settlement1, empty_settlement2, self.player1)

        with self.assertRaises(Exception) as context:
             self.board.add_settlement(empty_settlement3, self.player1)

             self.assertTrue('Settlements must be connected by roads' in str(context.exception))

    def test_non_touching_settlements(self):
        empty_settlement1 = self.board.settlements[3]
        empty_settlement2 = self.board.settlements[8]

        self.board.add_settlement(empty_settlement1, self.player1)
        self.board.add_settlement(empty_settlement2, self.player1)

        self.assertIsInstance(self.board.settlements[3], Settlement)
        self.assertIsInstance(self.board.settlements[8], Settlement)

if __name__ == "__main__":
    unittest.main()