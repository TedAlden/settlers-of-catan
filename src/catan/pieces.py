import pygame
from math import sin, cos, pi, sqrt
from .type import TerrainType


pygame.font.init()
FONT = pygame.font.SysFont(None, 32)
# TODO: make font renderer class


def draw_hexagon(surface, colour, radius, position, outline=None):
    x, y, r = *position, radius
    sides = [(x + r*cos(pi*i/3), y + r*sin(pi*i/3)) for i in range(6)]
    # draw filled hexagon
    pygame.draw.polygon(surface, colour, sides, width=0)
    if outline:
        # draw outline
        for a, b in [[0,1], [1,2], [2,3], [3,4], [4,5], [5,0]]:
            pygame.draw.aaline(surface, outline, sides[a], sides[b])


class Node(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.value = None


    def set_pos(self, x, y):
        self.rect.center = (x, y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])


    def __repr__(self):
        return self.__class__.__name__ + str(self.value)


class Terrain(Node):
 
    def __init__(self, axial_coord):
        super().__init__()
        self.axial_coord = axial_coord
        self.radius = 60
        height = self.radius * sqrt(3)
        self.image = pygame.Surface([self.radius * 2, height * 2])
        self.rect = self.image.get_rect()

        self.type = None
        self.number = -1


    def __repr__(self):
        return f"{self.__class__.__name__}({self.axial_coord[0]},{self.axial_coord[1]})"


    def draw(self, screen):
        col = "#5aa832"
        if self.type == TerrainType.FIELD: col = "#e6d85e"
        elif self.type == TerrainType.PASTURE: col = "#5fc73a"
        elif self.type == TerrainType.FOREST: col = "#168a35"
        elif self.type == TerrainType.HILL: col = "#e09e2b"
        elif self.type == TerrainType.MOUNTAIN: col = "#8c8c8c"
        elif self.type == TerrainType.DESERT: col = "#b5ac6e"

        draw_hexagon(screen, col, self.radius, self.get_pos(), outline="black")

        # draw the dice number on the terrain
        if self.number > 0:
            img = FONT.render(str(self.number), True, "white")
            w, h = img.get_rect().width, img.get_rect().height
            x, y = self.get_pos()
            x, y = x - 0.5 * w, y - 0.5 * h
            screen.blit(img, (x, y))


class Settlement(Node):

    def __init__(self, index):
        super().__init__()
        self.radius = 10
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.rect = self.image.get_rect()
        self.value = index
        self.selected = False
        self.owner = None


    def draw(self, screen):
        # TODO: change red to the colour of the current player
        if not self.owner:
            colour = "red" if self.selected else "#cccccc"
            pygame.draw.circle(screen, colour, self.get_pos(), self.radius)
        else:
            pygame.draw.circle(screen, "red", self.get_pos(), self.radius)


# TODO: make Road an object rather than just a (Settlement, Settlement)?