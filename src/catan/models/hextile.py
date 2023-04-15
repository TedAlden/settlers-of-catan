import pygame

from math import sqrt


class HexTile(pygame.sprite.Sprite):
 
    def __init__(self, axial_coord):
        super().__init__()
        self.axial_coord = axial_coord
        self.radius = 55
        height = self.radius * sqrt(3)
        self.image = pygame.Surface([self.radius * 2, height * 2])
        self.rect = self.image.get_rect()

        self.type = None
        self.number = -1


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])
