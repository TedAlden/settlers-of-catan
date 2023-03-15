from enum import Enum

# Forest (produces Lumber)
# Pasture (produces Wool)
# Field (produces Grain)
# Hill (produces Brick)
# Mountain (produces Ore)


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
    PLACE_ROAD = 1
    PLACE_SETTLEMENT = 2
    PLACE_CITY = 4
    PLACE_ROBBER = 8