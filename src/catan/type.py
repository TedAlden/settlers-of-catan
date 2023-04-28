from enum import Enum


class TerrainType(Enum):
    FOREST = 1
    PASTURE = 2
    FIELD = 4
    HILL = 8
    MOUNTAIN = 16
    DESERT = 32


class ResourceType(Enum):
    LUMBER = "Lumber"
    WOOL = "Wool"
    GRAIN = "Grain"
    BRICK = "Brick"
    ORE = "Ore"
    ANY = "Any"  # used for 3:1 harbours


class ActionType(Enum):
    NONE = "None"
    PLACE_ROAD = "Placing road"
    PLACE_SETTLEMENT = "Placing settlement"
    PLACE_CITY = "Placing city"
    PLACE_ROBBER = "Placing robber"


class GameMode(Enum):
    FIRST_TO_TEN = 1
    TIME_LIMIT = 2


class PlayerType(Enum):
    PLAYER = 1
    AI = 2
