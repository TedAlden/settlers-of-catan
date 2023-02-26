import pygame
from math import sqrt
from collections import defaultdict
from pieces import Terrain, Settlement


class Board:

    def __init__(self, hex_radius, tile_radius):
        self.tile_radius = tile_radius
        self.hex_radius = hex_radius
        self.hex_height = hex_radius * sqrt(3)
    
        self._graph = defaultdict(list)
        self.make_board()


    def make_board(self):
        self.settlements = [Settlement(i) for i in range(54)]
        self.roads = []

        self.terrain_tiles = {
            "0,-2": Terrain((0, -2)),
            "-1,-1": Terrain((-1, -1)),
            "1,-2": Terrain((1,-2)),
            "-2,0": Terrain((-2, 0)),
            "0,-1": Terrain((0, -1)),
            "2,-2": Terrain((2,-2)),
            "-1,0": Terrain((-1, 0)),
            "1,-1": Terrain((1,-1)),
            "-2,1": Terrain((-2, 1)),
            "0,0": Terrain((0, 0)),
            "2,-1": Terrain((2,-1)),
            "-1,1": Terrain((-1, 1)),
            "1,0": Terrain((1,0)),
            "-2,2": Terrain((-2, 2)),
            "0,1": Terrain((0, 1)),
            "2,0": Terrain((2,0)),
            "-1,2": Terrain((-1, 2)),
            "1,1": Terrain((1,1)),
            "0,2": Terrain((0, 2))
        }

        # map of each terrain tile to the indices of the settlements it
        # connects to, in a clock-wise direction starting top-right.
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

        # Used for working out the position of a settlement relative to
        # a terrain tile. Index 0 is the top right settlement, follows
        # in a clockwise direction to index 5 being the top left.
        relative_coords = [
            (self.hex_radius / 2, self.hex_height / 2),
            (self.hex_radius, 0),
            (self.hex_radius / 2, -(self.hex_height / 2)),
            (-(self.hex_radius / 2), -(self.hex_height / 2)),
            (-self.hex_radius, 0),
            (-(self.hex_radius / 2), self.hex_height / 2)
        ]

        # create connections for graph
        for terrain_coord, settlement_idxs in connections.items():
            # connect each settlement to the tile it is neighbouring
            for settlement_idx in settlement_idxs:
                self.add_edge(self.terrain_tiles[terrain_coord],
                            self.settlements[settlement_idx])
                
            # connect each surrounding settlement to eachother in a ring
            for idx1, idx2 in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)):
                self.add_edge(self.settlements[settlement_idxs[idx1]],
                              self.settlements[settlement_idxs[idx2]])
 
        visited_settlements = []
        for terrain_tile in self.terrain_tiles.values():
            # calculate screencoordinates for each terrain tile based on
            # its axial coordinate.
            tx, ty = terrain_tile.axial_coord
            x = tx * 3/2 * self.hex_radius
            y = tx * 0.5 * self.hex_height + ty * self.hex_height
            terrain_tile.screen_coord = (x + 300, y + 300)  # Offset grid

            # calculate screen coordinates for each settlement based on
            # which terrain tile it neighbours.
            for settlement in self.get_surrounding_nodes(terrain_tile):
                if settlement not in visited_settlements:
                    idx = self._graph[terrain_tile].index(settlement)
                        
                    x = terrain_tile.screen_coord[0] + relative_coords[idx][0]
                    y = terrain_tile.screen_coord[1] - relative_coords[idx][1]

                    settlement.screen_coord = (x, y)
                    visited_settlements.append(settlement)

        # testing:
        self.roads.append([self.settlements[0], self.settlements[3]])


    def get_terrain_tile(self, tile_x, tile_y):
        return self.terrain_tiles[f"{str(int(tile_x))},{str(int(tile_y))}"]


    def remove_edge(self, node1, node2):
        if node2 in self._graph[node1]:
            self._graph[node1].remove(node2)
        if node1 in self._graph[node2]:
            self._graph[node2].remove(node1)


    def add_edge(self, node1, node2):
        if node2 not in self._graph[node1]:
            self._graph[node1].append(node2)
        if node1 not in self._graph[node2]:
            self._graph[node2].append(node1)


    def has_connection(self, node1, node2):
        return node2 in self._graph[node1] or node1 in self._graph[node2]


    def has_road(self, node1, node2):
        return (node1, node2) in self.roads or (node2, node1) in self.roads


    def get_surrounding_nodes(self, node):
        return self._graph[node]


    def draw(self, screen):
        for terrain_tile in self.terrain_tiles.values():
            terrain_tile.draw(screen)

        for settlement in self.settlements:
            settlement.draw(screen)

        for node1, node2 in self.roads:
            pygame.draw.line(screen, "green", node1.screen_coord, node2.screen_coord, width=5)
