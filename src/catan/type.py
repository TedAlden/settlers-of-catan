from enum import Enum


class TerrainType(Enum):
    FOREST = 1
    PASTURE = 2
    FIELD = 4
    HILL = 8
    MOUNTAIN = 16
    DESERT = 32


class ResourceType(Enum):
    LUMBER = 1
    WOOL = 2
    GRAIN = 4
    BRICK = 8
    ORE = 16


class ActionType(Enum):
    NONE = "None"
    PLACE_ROAD = "Placing road"
    PLACE_SETTLEMENT = "Placing settlement"
    PLACE_CITY = "Placing city"
    PLACE_ROBBER = "Placing robber"


class GameMode(Enum):
    FIRST_TO_TEN = 1
    TIME_LIMIT = 2
