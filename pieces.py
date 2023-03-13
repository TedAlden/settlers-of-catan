import pygame
from math import sin, cos, pi, sqrt


pygame.font.init()
FONT = pygame.font.SysFont(None, 24)
# TODO: make font renderer class


def draw_hexagon(surface, colour, radius, position, width=0):
    x, y, r = *position, radius
    sides = [(x + r*cos(pi*i/3), y + r*sin(pi*i/3)) for i in range(6)]
    pygame.draw.polygon(surface, colour, sides, width)


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
        self.radius = 40
        height = self.radius * sqrt(3)
        self.image = pygame.Surface([self.radius * 2, height * 2])
        self.rect = self.image.get_rect()

        self.type = "forest" # TODO: use enum here
        # Forest (produces Lumber)
        # Pasture (produces Wool)
        # Field (produces Grain)
        # Hill (produces Brick)
        # Mountain (produces Ore)
        self.number = -1


    def __repr__(self):
        return f"{self.__class__.__name__}({self.axial_coord[0]},{self.axial_coord[1]})"


    def draw(self, screen):
        col = "#5aa832" # TODO: use default dict here instead of if/elif
        if self.type == "field": col = "#e6d85e"
        elif self.type == "pasture": col = "#5fc73a"
        elif self.type == "forest": col = "#168a35"
        elif self.type == "hill": col = "#e09e2b"
        elif self.type == "mountain": col = "#8c8c8c"
        elif self.type == "desert": col = "#b5ac6e"

        draw_hexagon(screen, col, self.radius, self.get_pos())

        if self.number > 0:
            img = FONT.render(str(self.number), True, "white")
            w, h = img.get_rect().width, img.get_rect().height
            x, y = self.get_pos()
            x, y = x - 0.5 * w, y - 0.5 * w
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
        col = "red" if self.selected else "#aaaaaa"
        # TODO: change green to the colour of the current player
        pygame.draw.circle(screen, col, self.get_pos(), self.radius)
