import pygame
from math import sin, cos, pi


def draw_settlement(surface, colour, position, outline=None):
    x, y = position
    sides = [(x-10,y+10),(x-10,y+0),(x+0,y-10),(x+10,y+0),(x+10,y+10)]
    pygame.draw.polygon(surface, colour, sides, width=0)
    if outline:
        n = len(sides)
        for a, b in [*zip(range(n), range(n)[1:]), (n-1, 0)]:
            pygame.draw.aaline(surface, outline, sides[a], sides[b])


def draw_city(surface, colour, position, outline=None):
    x, y = position
    sides = [(x-15,y+10),(x-15,y-5),(x-5,y-15),(x+5,y-5),(x+15,y-5),(x+15,y+10)]
    pygame.draw.polygon(surface, colour, sides, width=0)
    if outline:
        n = len(sides)
        for a, b in [*zip(range(n), range(n)[1:]), (n-1, 0)]:
            pygame.draw.aaline(surface, outline, sides[a], sides[b])


def draw_hexagon(surface, colour, radius, position, outline=None):
    x, y, r = *position, radius
    sides = [(x + r*cos(pi*i/3), y + r*sin(pi*i/3)) for i in range(6)]
    pygame.draw.polygon(surface, colour, sides, width=0)
    if outline:
        n = len(sides)
        for a, b in [*zip(range(n), range(n)[1:]), (n-1, 0)]:
            pygame.draw.aaline(surface, outline, sides[a], sides[b])