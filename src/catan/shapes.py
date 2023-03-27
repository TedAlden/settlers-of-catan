import pygame
from math import sin, cos, pi


DICE_DOTS = {
    1: [(32, 32)],
    2: [(16, 16), (48, 48)],
    3: [(16, 16), (32, 32), (48, 48)],
    4: [(16, 16), (16, 48), (48, 16), (48, 48)],
    5: [(16, 16), (16, 48), (48, 16), (48, 48), (32, 32)],
    6: [(16, 16), (16, 48), (48, 16), (48, 48), (16, 32), (48, 32)]
}


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


def draw_dice(surface, position, number):
    x, y = position
    sides = [(x-32,y-32), (x+32,y-32), (x+32,y+32), (x-32,y+32)]
    pygame.draw.rect(surface, "white", (x-32, y-32, 64, 64))
    pygame.draw.rect(surface, "black", (x-32, y-32, 64, 64), width=2)

    number = number if number in range(1, 7) else 6 # default

    for x1, y1 in DICE_DOTS.get(number):
        pygame.draw.circle(surface, "black", (x+x1-32, y+y1-32), 7)

    