import pygame
from math import pi, sin, cos, sqrt


def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)


def draw_hexagon(surface, colour, radius, position, width=0):
    return draw_regular_polygon(surface, colour, 6, radius, position, width)


class Board:

    def __init__(self, hex_radius, tile_radius):
        """
        Constructor for hexagonal board. Note that `hex_radius` designates the
        size of the spaces for the tiles, and `tile_radius` designates the size
        of the tiles themselves, so `tile_radius` must be less than or equal to
        `hex_radius` in order for tiles to fit in their spaces.

        Args:
            hex_radius: The hexagonal radius of the spaces for the tiles.
            tile_radius. The hexagonal radious of the tiles themselves.
        """
        self.hex_radius = hex_radius
        self.hex_height = hex_radius * sqrt(3)
        self.tile_radius = tile_radius

    def draw(self, screen):
        for i in range(13):
            for j in range(4):
                x = 3 * self.hex_radius * j
                x += 1.5 * self.hex_radius if i % 2 == 0 else 0 # Every 2nd row,
                # add an offset to the x coord so that the hexagons interlock.
                y = 0.5 * self.hex_height * i
                draw_hexagon(screen, "red", self.tile_radius, (x, y))
