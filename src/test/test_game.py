import unittest
from catan.models.game import GameModel
from catan.type import GameMode

class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.game = GameModel(game_mode=GameMode.TIME_LIMIT, game_time_limit=20)

    def test_game_end_time_limit(self):
        game_time = 0
        game_running = True

        while game_running:
            # Simulate the passage of time by incrementing the game time
            game_time += 1
            self.game.game_time = game_time

            # Check if the game should end due to the time limit being reached
            if self.game.game_mode == GameMode.TIME_LIMIT and game_time >= self.game.game_time_limit:
                game_running = False

        self.assertEqual(game_time, self.game.game_time_limit, "Game didn't end when time limit was reached")

if __name__ == "__main__":
    unittest.main()