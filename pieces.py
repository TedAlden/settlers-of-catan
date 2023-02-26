import pygame
from math import sin, cos, pi


def draw_hexagon(surface, colour, radius, position, width=0):
    x, y, r = *position, radius
    sides = [(x + r*cos(pi*i/3), y + r*sin(pi*i/3)) for i in range(6)]
    pygame.draw.polygon(surface, colour, sides, width)


class Node:

    def __init__(self, value):
        self.value = value
        self.screen_coord = (0, 0)

    def __repr__(self):
        return self.__class__.__name__ + str(self.value)


class Terrain(Node):
 
    def __init__(self, axial_coord):
        super().__init__(None)
        self.axial_coord = axial_coord
        self.tile_radius = 25

    def __repr__(self):
        return f"{self.__class__.__name__}({self.axial_coord[0]},{self.axial_coord[1]})"

    def draw(self, screen):
        draw_hexagon(screen, "red", self.tile_radius, self.screen_coord)


class Settlement(Node):

    def __init__(self, value):
        super().__init__(value)

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.screen_coord, 5)
