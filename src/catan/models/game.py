import jsonpickle

from catan.models.board import Board
from catan.models.player import Player
from catan.models.bank import Bank
from catan.models.dice import Dice
from catan.models.robber import Robber
from catan.type import GameMode, PlayerType


class GameModel:

    def __init__(self,
                 game_mode = GameMode.FIRST_TO_TEN,
                 game_time_limit = -1,
                 player_1_type = PlayerType.PLAYER,
                 player_2_type = PlayerType.PLAYER,
                 player_3_type = PlayerType.PLAYER,
                 player_4_type = PlayerType.PLAYER,
                 player_1_name = "Player 1",
                 player_2_name = "Player 2",
                 player_3_name = "Player 3",
                 player_4_name = "Player 4",
                 player_1_colour = "red",
                 player_2_colour = "green",
                 player_3_colour = "blue",
                 player_4_colour = "purple"
                 ):

        # Game objects
        self.game_time = 0
        self.game_time_limit = game_time_limit
        self.game_mode = game_mode
        self.board = Board.make_random()
        self.bank = Bank()
        self.robber = Robber()
        self.dice1 = Dice()
        self.dice2 = Dice()
        self.players = []

        if player_1_type == PlayerType.AI:
            self.players.append(Player(player_1_name, player_1_colour))
        else:
            self.players.append(Player(player_1_name, player_1_colour))

        if player_2_type == PlayerType.AI:    
            self.players.append(Player(player_2_name, player_2_colour))
        else:
            self.players.append(Player(player_2_name, player_2_colour))

        if player_3_type == PlayerType.AI:
            self.players.append(Player(player_3_name, player_3_colour))
        else:
            self.players.append(Player(player_3_name, player_3_colour))

        if player_4_type == PlayerType.AI:
            self.players.append(Player(player_4_name, player_4_colour))
        else:
            self.players.append(Player(player_4_name, player_4_colour))

        self.current_turn = self.players[0]

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
