import pygame
from math import pi, sin, cos, sqrt
from collections import defaultdict
from pieces import Terrain, Settlement


def draw_hexagon(surface, colour, radius, position, width=0):
    x, y = position
    sides = [(x + radius*cos(pi*i/3), y + radius*sin(pi*i/3)) for i in range(6)]
    pygame.draw.polygon(surface, colour, sides, width)


class Board:

    def __init__(self, hex_radius, tile_radius):
        """
        Constructor for hexagonal board. Note that `hex_radius`
        designates the size of the spaces for the tiles, and
        `tile_radius` designates the size of the tiles themselves, so
        `tile_radius` must be less than or equal to `hex_radius` in
        order for tiles to fit in their spaces.

        Args:
            hex_radius: The hexagonal radius of the spaces for the tiles.
            tile_radius. The hexagonal radious of the tiles themselves.
        """
        self.hex_radius = hex_radius
        self.hex_height = hex_radius * sqrt(3)
        self.tile_radius = tile_radius

        self._graph = defaultdict(list)

        # Used for working out the position of a settlement relative to
        # a terrain tile. Index 0 is the top right settlement, follows
        # in a clockwise direction to index 5 being the top left.
        self.xy = [
            (self.hex_radius / 2, self.hex_height / 2),
            (self.hex_radius, 0),
            (self.hex_radius / 2, -(self.hex_height / 2)),
            (-(self.hex_radius / 2), -(self.hex_height / 2)),
            (-self.hex_radius, 0),
            (-(self.hex_radius / 2), self.hex_height / 2)
        ]

        self.make_board()

    def make_board(self):
        # 2D list would've been syntactically better, e.g. using
        # self.terrain_tiles[-2][0], howwever, a hashmap requires less
        # wrapper code here, i.e. using negative indices with a 2D list.
        self.terrain_tiles = {
            "-2,0": Terrain((-2, 0)),
            "-2,1": Terrain((-2, 1)),
            "-2,2": Terrain((-2, 2)),
            "-1,-1": Terrain((-1, -1)),
            "-1,0": Terrain((-1, 0)),
            "-1,1": Terrain((-1, 1)),
            "-1,2": Terrain((-1, 2)),
            "0,-2": Terrain((0, -2)),
            "0,-1": Terrain((0, -1)),
            "0,0": Terrain((0, 0)),
            "0,1": Terrain((0, 1)),
            "0,2": Terrain((0, 2)),
            "1,-2": Terrain((1,-2)),
            "1,-1": Terrain((1,-1)),
            "1,0": Terrain((1,0)),
            "1,1": Terrain((1,1)),
            "2,-2": Terrain((2,-2)),
            "2,-1": Terrain((2,-1)),
            "2,0": Terrain((2,0))
        }

        self.settlements = [Settlement(i) for i in range(54)]
        # Roads will be added as tuple pairs (Settlement, Settlement),
        # rather than actually existing on the graph itself.
        self.roads = []
        self.roads.append([self.settlements[0], self.settlements[3]])

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

        # create connections for settlements and tiles.
        for terrain_coord, settlement_idxs in connections.items():
            # 1. connect each settlement to the tile it is surrounding
            for settlement_idx in settlement_idxs:
                self.add_edge(self.terrain_tiles[terrain_coord],
                            self.settlements[settlement_idx])
                
            # 2. connect each settlement to eachother in a ringe shape
            # around the terrain tile.
            for idx1, idx2 in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)):
                self.add_edge(self.settlements[settlement_idxs[idx1]],
                              self.settlements[settlement_idxs[idx2]])
 
        # Calculate screen/pixel coordinates for each terrain tile,
        # based on it's hexagonal tile coordinate.
        for _, terrain_tile in self.terrain_tiles.items():
            tx, ty = terrain_tile.tile_coord
            x = tx * 3/2 * self.hex_radius
            y = tx * 0.5 * self.hex_height + ty * self.hex_height
            x += 300
            y += 300
            terrain_tile.coord = (x, y)


    def get_terrain_tile(self, tile_x, tile_y):
        return self.terrain_tiles[f"{str(int(tile_x))},{str(int(tile_y))}"]


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


    def draw_hexagons(self, screen):
        # Deprecated. Previously used to draw array of hexagons on the
        # screen.
        for i in range(13):
            for j in range(4):
                x = 3 * self.hex_radius * j
                x += 1.5 * self.hex_radius if i % 2 == 0 else 0 # Every 2nd row,
                # add an offset to the x coord so that the hexagons interlock.
                y = 0.5 * self.hex_height * i
                draw_hexagon(screen, "red", self.tile_radius, (x, y))
    

    def draw(self, screen):
        visited = []

        for hex_coord, terrain_tile in self.terrain_tiles.items():
            draw_hexagon(screen, "red", 25, terrain_tile.coord)

            for settlement in self.get_surrounding_nodes(terrain_tile):
                idx = self._graph[terrain_tile].index(settlement)
                    
                x = terrain_tile.coord[0] + self.xy[idx][0]
                y = terrain_tile.coord[1] + self.xy[idx][1]

                settlement.coord = (x, y)
                pygame.draw.circle(screen, "blue", (x, y), 5)
                visited.append(settlement)
        
        for node1, node2 in self.roads:
            pygame.draw.line(screen, "green", node1.coord, node2.coord, width=5)


# TODO: change the coords of nodes to be NamedTuples instead of lists.

# TODO: merge self.terrain_tiles and the connections hashmap into one
# data structure. May allow for importing and exporting maps?