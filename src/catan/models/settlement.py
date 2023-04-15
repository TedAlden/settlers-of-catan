import pygame

from catan.util.shapes import draw_settlement


class Settlement(pygame.sprite.Sprite):

    def __init__(self, index, owner):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.value = index
        self.owner = owner
        self.selected = False


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])
