import pygame

from catan.util.shapes import draw_city


class City(pygame.sprite.Sprite):

    def __init__(self, index, owner):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.value = index
        self.selected = False
        self.owner = owner


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])
