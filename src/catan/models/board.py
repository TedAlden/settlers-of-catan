from math import sqrt
from collections import defaultdict
from random import shuffle

from catan.models.harbour import Harbour
from catan.models.settlement import Settlement
from catan.models.emptysettlement import EmptySettlement
from catan.models.hextile import HexTile
from catan.models.road import Road
from catan.models.city import City
from catan.type import ResourceType, TerrainType


class Board:

    def __init__(self):
        self._graph = defaultdict(list)
        self.settlements = []
        self.roads = []
        self.terrain_tiles = {}
        self.harbours = {}


    def get_terrain_tile(self, axial_x, axial_y):
        return self.terrain_tiles[f"{str(int(axial_x))},{str(int(axial_y))}"]


    def add_settlement(self, empty_settlement, owner):
        if isinstance(empty_settlement, EmptySettlement):
            settlement = Settlement(empty_settlement.value, owner)
            settlement.set_pos(*empty_settlement.get_pos())

            # replace graph connections referring to the empty
            # settlement with the new settlement
            for node, connections in self._graph.items():
                if empty_settlement in connections:
                    i = connections.index(empty_settlement)
                    connections[i] = settlement
                    self._graph[node] = connections
            
            # update dict keys from empty settlement to new settlement
            self._graph[settlement] = self._graph[empty_settlement]
            del self._graph[empty_settlement]

            # update list of settlements
            index = self.settlements.index(empty_settlement)
            self.settlements[index] = settlement

            # replace references to this settlement in any roads, to
            # refer to the city instead
            for road in self.roads:
                if empty_settlement in road.settlements:
                    index = road.settlements.index(empty_settlement)
                    road.settlements[index] = settlement

    
    def remove_settlement(self, node):
        raise NotImplementedError
    

    def add_city(self, settlement):
        if isinstance(settlement, Settlement):
            city = City(settlement.value, settlement.owner)
            city.set_pos(*settlement.get_pos())

            # replace graph connections referring to the old settlement
            # with the new city
            for node, connections in self._graph.items():
                if settlement in connections:
                    i = connections.index(settlement)
                    connections[i] = city
                    self._graph[node] = connections
            
            # update dict keys from old settlement to new city
            self._graph[city] = self._graph[settlement]
            del self._graph[settlement]

            # update list of settlements
            index = self.settlements.index(settlement)
            self.settlements[index] = city

            # replace references to this settlement in any roads, to
            # refer to the city instead
            for road in self.roads:
                if settlement in road.settlements:
                    index = road.settlements.index(settlement)
                    road.settlements[index] = city


    def get_road_owner(self, node1, node2):
        for road in self.roads:
            if node1 in road.settlements and node2 in road.settlements:
                return road.owner


    def add_edge(self, node1, node2):
        if node2 not in self._graph[node1]:
            self._graph[node1].append(node2)
        if node1 not in self._graph[node2]:
            self._graph[node2].append(node1)


    def remove_edge(self, node1, node2):
        if node2 in self._graph[node1]:
            self._graph[node1].remove(node2)
        if node1 in self._graph[node2]:
            self._graph[node2].remove(node1)


    def has_edge(self, node1, node2):
        return node2 in self._graph[node1] or node1 in self._graph[node2]


    def add_road(self, node1, node2, owner):
        self.roads.append(Road(node1, node2, owner))

    
    def remove_road(self, node1, node2):
        for road in self.roads:
            if node1 in road.settlements and node2 in road.settlements:
                self.roads.remove(road)


    def has_road(self, node1, node2):
        for road in self.roads:
            if node1 in road.settlements and node2 in road.settlements:
                return True
            
        return False


    def get_surrounding_nodes(self, node):
        return self._graph[node]


    @staticmethod
    def make_random():
        b = Board()
        b.settlements = [EmptySettlement(i) for i in range(54)]
        b.roads = []
        b.terrain_tiles = {
            "0,-2": HexTile((0, -2)),
            "-1,-1": HexTile((-1, -1)),
            "1,-2": HexTile((1,-2)),
            "-2,0": HexTile((-2, 0)),
            "0,-1": HexTile((0, -1)),
            "2,-2": HexTile((2,-2)),
            "-1,0": HexTile((-1, 0)),
            "1,-1": HexTile((1,-1)),
            "-2,1": HexTile((-2, 1)),
            "0,0": HexTile((0, 0)),
            "2,-1": HexTile((2,-1)),
            "-1,1": HexTile((-1, 1)),
            "1,0": HexTile((1,0)),
            "-2,2": HexTile((-2, 2)),
            "0,1": HexTile((0, 1)),
            "2,0": HexTile((2,0)),
            "-1,2": HexTile((-1, 2)),
            "1,1": HexTile((1,1)),
            "0,2": HexTile((0, 2))
        }

        # TODO: change terrain_tiles to a list instead?

        # hard-coded map of each terrain to the indices of the
        # settlements it is connected to. clock-wise, starting top-right
        connections = {
            "-2,0": [7, 13, 19, 18, 12, 6],
            "-2,1": [19, 25, 31, 30, 24, 18],
            "-2,2": [31, 37, 43, 42, 36, 30],
            "-1,-1": [3, 8, 14, 13, 7, 2],
            "-1,0": [14, 20, 26, 25, 19, 13],
            "-1,1": [26, 32, 38, 37, 31, 25],
            "-1,2": [38, 44, 49, 48, 43, 37],
            "0,-2": [1, 4, 9, 8, 3, 0],
            "0,-1": [9, 15, 21, 20, 14, 8],
            "0,0": [21, 27, 33, 32, 26, 20],
            "0,1": [33, 39, 45, 44, 38, 32],
            "0,2": [45, 50, 53, 52, 49, 44],
            "1,-2": [5, 10, 16, 15, 9, 4],
            "1,-1": [16, 22, 28, 27, 21, 15],
            "1,0": [28, 34, 40, 39, 33, 27],
            "1,1": [40, 46, 51, 50, 45, 39],
            "2,-2": [11, 17, 23, 22, 16, 10],
            "2,-1": [23, 29, 35, 34, 28, 22],
            "2,0": [35, 41, 47, 46, 40, 34]
        }

        # ----------- add harbours -------------------------------------
        harbour_types = [ResourceType.ANY,
                         ResourceType.ANY,
                         ResourceType.ANY,
                         ResourceType.ANY,
                         ResourceType.LUMBER,
                         ResourceType.WOOL,
                         ResourceType.GRAIN,
                         ResourceType.BRICK,
                         ResourceType.ORE]
        
        shuffle(harbour_types)
        
        b.harbours = {
            "0,-3": Harbour((0, -3), harbour_types[0], b.settlements[0], b.settlements[0]),
            "2,-3": Harbour((2, -3), harbour_types[1], b.settlements[5], b.settlements[10]),
            "3,-2": Harbour((3, -2), harbour_types[2], b.settlements[23], b.settlements[29]),
            "3,0": Harbour((3, 0), harbour_types[3], b.settlements[41], b.settlements[47]),
            "1,2": Harbour((1, 2), harbour_types[4], b.settlements[50], b.settlements[51]),
            "-1,3": Harbour((-1, 3), harbour_types[5], b.settlements[48], b.settlements[49]),
            "-3,3": Harbour((-3, 3), harbour_types[6], b.settlements[36], b.settlements[42]),
            "-3,1": Harbour((-3, 1), harbour_types[7], b.settlements[18], b.settlements[24]),
            "-2,-1": Harbour((-2, -1), harbour_types[8], b.settlements[2], b.settlements[7]),
        }        

        # ----------- create connections in the graph ------------------
        for terrain_coord, settlement_idxs in connections.items():
            # connect each settlement to the terrain it is neighbouring
            for settlement_idx in settlement_idxs:
                b.add_edge(b.terrain_tiles[terrain_coord],
                            b.settlements[settlement_idx])
            # connect each surrounding settlement to eachother in a ring
            for idx1, idx2 in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)):
                b.add_edge(b.settlements[settlement_idxs[idx1]],
                              b.settlements[settlement_idxs[idx2]])

        # ----------- assign resource types and numbers to terrains ----
        numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        types = [TerrainType.FOREST, TerrainType.FOREST, TerrainType.FOREST,
                 TerrainType.FOREST, TerrainType.PASTURE, TerrainType.PASTURE,
                 TerrainType.PASTURE, TerrainType.PASTURE, TerrainType.FIELD,
                 TerrainType.FIELD, TerrainType.FIELD, TerrainType.FIELD,
                 TerrainType.HILL, TerrainType.HILL, TerrainType.HILL,
                 TerrainType.MOUNTAIN, TerrainType.MOUNTAIN,
                 TerrainType.MOUNTAIN
                 ]

        # first place the desert terrain in the center of the board
        _terrains = b.terrain_tiles.copy()
        desert_terrain = _terrains.pop("0,0")
        desert_terrain.type = TerrainType.DESERT

        # randomly place other terrains and assign random dice numbers
        terrains = list(_terrains.values())
        shuffle(types)
        shuffle(numbers)

        for i in range(18):
            terrains[i].type = types[i]
            terrains[i].number = numbers[i]

        return b
