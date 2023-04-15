import pygame

from catan.util.shapes import draw_dice


class DiceView(pygame.sprite.Sprite):

    def __init__(self, model, topleft):
        super().__init__()
        self.model = model
        self.surf = pygame.Surface((64, 64))
        self.rect = self.surf.get_rect()
        self.rect.topleft = topleft


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])


    def roll(self):
        self.model.roll()


    def draw(self, screen):
        draw_dice(screen, self.rect.topleft, self.model.value)