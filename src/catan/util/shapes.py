import pygame

from math import sin, cos, pi


pygame.font.init()
TERRAIN_NUMBER_FONT = pygame.font.SysFont(None, 32)

DICE_DOTS = {
    1: [(0, 0)],
    2: [(-16, -16), (16, 16)],
    3: [(-16, -16), (16, 16), (0, 0)],
    4: [(-16, -16), (16, 16), (-16, 16), (16, -16)],
    5: [(-16, -16), (16, 16), (-16, 16), (16, -16), (0, 0)],
    6: [(-16, -16), (16, 16), (-16, 16), (16, -16), (-16, 0), (16, 0)]
}

DICE_VERTICES = [
    (-32, -32),
    (-32, +32),
    (+32, +32),
    (+32, -32),
]

SETTLEMENT_VERTICES = [
    (-10, +10),
    (-10, -5),
    (+0, -15),
    (+10, -5),
    (+10, +10)
]

CITY_VERTICES = [
    (-15, +10),
    (-15, -5),
    (-5, -15),
    (+5, -5),
    (+15, -5),
    (+15, +10)
]

ROBBER_VERTICES = [
    (-7, -5),
    (-3, -5),
    (-3, -10),
    (+3, -10),
    (+3, -5),
    (+7, -5),
    (+7, +5),
    (+5, +5),
    (+5, +10),
    (-5, +10),
    (-5, +5),
    (-7, +5)
]


def get_side_vertex_indices(n):
    return [*zip(range(n), range(n)[1:]), (n-1, 0)]


def draw_settlement(surface, colour, position):
    x, y = position
    vertices = [(_x + x, _y + y) for (_x, _y) in SETTLEMENT_VERTICES]
    # draw settlement shape
    pygame.draw.polygon(surface, colour, vertices, width=0)
    # draw outline
    for a, b in get_side_vertex_indices(len(vertices)):
        pygame.draw.aaline(surface, "black", vertices[a], vertices[b])


def draw_city(surface, colour, position):
    x, y = position
    vertices = [(_x + x, _y + y) for (_x, _y) in CITY_VERTICES]
    # draw city shape
    pygame.draw.polygon(surface, colour, vertices, width=0)
    # draw outline
    for a, b in get_side_vertex_indices(len(vertices)):
        pygame.draw.aaline(surface, "black", vertices[a], vertices[b])


def draw_hextile(surface, colour, radius, position, number):
    x, y, r = *position, radius
    vertices = [(x + r*cos(pi*i/3), y + r*sin(pi*i/3)) for i in range(6)]
    # draw hexagon
    pygame.draw.polygon(surface, colour, vertices, width=0)
    # draw outline
    for a, b in get_side_vertex_indices(len(vertices)):
        pygame.draw.aaline(surface, "black", vertices[a], vertices[b])
    # draw hextile dice number if valid
    if number > 0:
        img = TERRAIN_NUMBER_FONT.render(str(number), True, "white")
        w, h = img.get_rect().width, img.get_rect().height
        surface.blit(img, (x - 0.5 * w, y - 0.5 * h))


def draw_robber(surface, position, colour):
    x, y = position
    vertices = [(_x + x, _y + y) for (_x, _y) in ROBBER_VERTICES]
    # draw robber shape
    pygame.draw.polygon(surface, colour, vertices, width=0)
    # draw outline
    for a, b in get_side_vertex_indices(len(vertices)):
        pygame.draw.aaline(surface, "black", vertices[a], vertices[b])


def draw_dice(surface, position, number):
    x, y = position
    vertices = [(_x + x, _y + y) for (_x, _y) in DICE_VERTICES]
    # draw square
    pygame.draw.polygon(surface, "white", vertices, width=0)
    # draw outline
    for a, b in get_side_vertex_indices(len(vertices)):
        pygame.draw.aaline(surface, "black", vertices[a], vertices[b])

    # draw dice dots
    number = number if number in range(1, 7) else 6 # default
    for _x, _y in DICE_DOTS.get(number):
        pygame.draw.circle(surface, "black", (x + _x, y + _y), 7)


def draw_road(surface, position1, position2, colour):
    # draw line for road
    pygame.draw.line(surface, colour, position1, position2, width=12)
    # draw circles either end of line to round it off
    pygame.draw.circle(surface, colour, position1, 5)
    pygame.draw.circle(surface, colour, position2, 5)
