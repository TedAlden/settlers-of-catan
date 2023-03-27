import pygame
import random
from math import sqrt
from .type import TerrainType
from .shapes import draw_settlement, draw_city, draw_hexagon, draw_dice


pygame.font.init()
TERRAIN_FONT = pygame.font.SysFont(None, 32)
# TODO: make font renderer class


class Sprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])


class Terrain(Sprite):
 
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
            img = TERRAIN_FONT.render(str(self.number), True, "white")
            w, h = img.get_rect().width, img.get_rect().height
            x, y = self.get_pos()
            x, y = x - 0.5 * w, y - 0.5 * h
            screen.blit(img, (x, y))


class EmptySettlement(Sprite):

    def __init__(self, index):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.value = index
        self.owner = None
        self.selected = False

    
    def draw(self, screen):
        colour = "#ffffff" if self.selected else "#cccccc"
        pygame.draw.circle(screen, colour, self.get_pos(), 10)


class Settlement(Sprite):

    def __init__(self, index, owner):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.value = index
        self.owner = owner
        self.selected = False


    def draw(self, screen):
        colour = "#ffffff" if self.selected else self.owner.colour
        draw_settlement(screen, colour, self.get_pos(), outline="black")


class City(Sprite):

    def __init__(self, index, owner):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.value = index
        self.selected = False
        self.owner = owner


    def draw(self, screen):
        colour = "#ffffff" if self.selected else self.owner.colour
        draw_city(screen, colour, self.get_pos(), outline="black")


class Road(Sprite):
    
    def __init__(self, node1, node2, owner):
        self.settlements = (node1, node2)
        self.owner = owner


    def draw(self, screen):
        pygame.draw.line(screen, self.owner.colour, self.settlements[0].get_pos(), self.settlements[1].get_pos(), width=8)


class Dice(Sprite):

    def __init__(self, center_x, center_y):
        super().__init__()
        self.value = 6
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)


    def roll(self):
        self.value = random.randint(1, 6)


    def draw(self, screen):
        draw_dice(screen, self.get_pos(), self.value)
