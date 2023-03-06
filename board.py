import pygame
import jsonpickle
from math import sqrt
from collections import defaultdict
from pieces import Terrain, Settlement


class Board:

    def __init__(self, hex_radius):
        self.hex_radius = hex_radius
        self.hex_height = hex_radius * sqrt(3)
        self._graph = defaultdict(list)


    def get_terrain_tile(self, axial_x, axial_y):
        return self.terrain_tiles[f"{str(int(axial_x))},{str(int(axial_y))}"]


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


    def add_road(self, node1, node2):
        self.roads.append([node1, node2])

    
    def remove_road(self, node1, node2):
        self.roads.remove([node1,])


    def has_road(self, node1, node2):
        return (node1, node2) in self.roads or (node2, node1) in self.roads


    def get_surrounding_nodes(self, node):
        return self._graph[node]


    def render(self, screen):
        for terrain_tile in self.terrain_tiles.values():
            terrain_tile.draw(screen)

        for settlement in self.settlements:
            settlement.draw(screen)

        for node1, node2 in self.roads:
            pygame.draw.line(screen, "green", node1.screen_coord, node2.screen_coord, width=12)


    @staticmethod
    def serialize(board):
        return jsonpickle.encode(board)


    @staticmethod
    def deserialize(pickle):
        return jsonpickle.decode(pickle)


    @staticmethod
    def save_to_file(board, path):
        with open(path, "w") as file:
            file.write(board.serialize())


    @staticmethod
    def load_from_file(path):
        with open(path, "r") as file:
            return Board.deserialize(file.read())


    @staticmethod
    def make_random():
        b = Board(50)

        b.settlements = [Settlement(i) for i in range(54)]
        b.roads = []
        b.terrain_tiles = {
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

        # position of a settlement relative to the terrain it surrounds.
        # clock-wise, starting top-right.
        relative_coords = [
            (b.hex_radius / 2, b.hex_height / 2),
            (b.hex_radius, 0),
            (b.hex_radius / 2, -(b.hex_height / 2)),
            (-(b.hex_radius / 2), -(b.hex_height / 2)),
            (-b.hex_radius, 0),
            (-(b.hex_radius / 2), b.hex_height / 2)
        ]

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

        # ----------- calculate coordinates of components --------------
        visited_settlements = []
        for terrain_tile in b.terrain_tiles.values():
            # convert axial terrain coords to screen/pixel coords.
            tx, ty = terrain_tile.axial_coord
            x = tx * 3/2 * b.hex_radius
            y = tx * 0.5 * b.hex_height + ty * b.hex_height
            terrain_tile.screen_coord = (x + 640, y + 400)  # shift grid
            # calculate screen coords for each settlement based on the
            # terrain that it neighbours.
            for settlement in b.get_surrounding_nodes(terrain_tile):
                if settlement not in visited_settlements:
                    idx = b._graph[terrain_tile].index(settlement)
                    x = terrain_tile.screen_coord[0] + relative_coords[idx][0]
                    y = terrain_tile.screen_coord[1] - relative_coords[idx][1]
                    settlement.screen_coord = (x, y)
                    visited_settlements.append(settlement)

        # ----------- add example roads --------------------------------
        b.add_road(b.settlements[0], b.settlements[3])
        b.add_road(b.settlements[8], b.settlements[3])
        b.add_road(b.settlements[2], b.settlements[3])
        b.add_road(b.settlements[8], b.settlements[14])

        b.add_road(b.settlements[35], b.settlements[41])
        b.add_road(b.settlements[41], b.settlements[47])

        b.add_road(b.settlements[30], b.settlements[36])
        b.add_road(b.settlements[36], b.settlements[42])
        b.add_road(b.settlements[42], b.settlements[43])

        return b