import pygame

from catan.util.shapes import draw_dice
from catan.util.pathresolver import resolve_path

DICE1 = pygame.image.load(resolve_path("catan/assets/images/dice_1.png"))
DICE2 = pygame.image.load(resolve_path("catan/assets/images/dice_2.png"))
DICE3 = pygame.image.load(resolve_path("catan/assets/images/dice_3.png"))
DICE4 = pygame.image.load(resolve_path("catan/assets/images/dice_4.png"))
DICE5 = pygame.image.load(resolve_path("catan/assets/images/dice_5.png"))
DICE6 = pygame.image.load(resolve_path("catan/assets/images/dice_6.png"))


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
        
        # image = DICE6 # default

        # if self.model.value == 1:
        #     image = DICE1
        # elif self.model.value == 2:
        #     image = DICE2
        # elif self.model.value == 3:
        #     image = DICE3
        # elif self.model.value == 4:
        #     image = DICE4
        # elif self.model.value == 5:
        #     image = DICE5
        # elif self.model.value == 6:
        #     image = DICE6
        
        # screen.blit(image, self.rect.topleft)