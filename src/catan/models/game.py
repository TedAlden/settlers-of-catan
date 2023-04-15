import jsonpickle

from catan.models.board import Board
from catan.models.player import Player
from catan.models.bank import Bank
from catan.models.dice import Dice
from catan.models.robber import Robber


class GameModel:

    def __init__(self):
        # Game objects
        self.game_time = 0
        self.board = Board.make_random()
        self.bank = Bank()
        self.robber = Robber()
        self.dice1 = Dice()
        self.dice2 = Dice()
        self.players = [
            Player("Player 1", "red"),
            Player("Player 2", "green"),
            Player("Player 3", "blue"),
            Player("Player 4", "purple")
        ]


    @staticmethod
    def serialize(game):
        return jsonpickle.encode(game, keys=True)


    @staticmethod
    def deserialize(pickle):
        return jsonpickle.decode(pickle, keys=True)


    @staticmethod
    def save_to_file(game, path):
        with open(path, "w") as file:
            file.write(GameModel.serialize(game))


    @staticmethod
    def load_from_file(path):
        with open(path, "r") as file:
            return GameModel.deserialize(file.read())
