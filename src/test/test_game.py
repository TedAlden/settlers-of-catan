import unittest
import os
from game import GameModel  


class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.game = GameModel()

    def test_serialize_and_deserialize(self):
        serialized_game = GameModel.serialize(self.game)
        deserialized_game = GameModel.deserialize(serialized_game)

        self.assertEqual(self.game.game_time, deserialized_game.game_time, "Failed to serialize and deserialize game_time correctly")
        self.assertEqual(self.game.game_time_limit, deserialized_game.game_time_limit, "Failed to serialize and deserialize game_time_limit correctly")
        self.assertEqual(self.game.game_mode, deserialized_game.game_mode, "Failed to serialize and deserialize game_mode correctly")

    def test_save_and_load_from_file(self):
        file_path = "test_game_model_save.json"

        GameModel.save_to_file(self.game, file_path)
        loaded_game = GameModel.load_from_file(file_path)

        self.assertEqual(self.game.game_time, loaded_game.game_time, "Failed to save and load game_time correctly")
        self.assertEqual(self.game.game_time_limit, loaded_game.game_time_limit, "Failed to save and load game_time_limit correctly")
        self.assertEqual(self.game.game_mode, loaded_game.game_mode, "Failed to save and load game_mode correctly")

        os.remove(file_path)  # Clean up the test file after the test


if __name__ == '__main__':
    unittest.main()

