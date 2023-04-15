import pygame

FONT_PATH = "src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf"
FONT_SIZE = 18
# FONT_PATH = "src\\catan\\assets\\fonts\\WashingtonText.ttf"
# FONT_SIZE = 24


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left, colour="white", background=None):
        self.text = text
        self.colour = colour
        self.background = background
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.surf = pygame.Surface((220, 50))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left
    
        self.text = self.font.render(self.text, True, self.colour, self.background)
        text_rect = self.text.get_rect()
        text_x = (self.rect.width / 2) - (text_rect.width / 2)
        text_y = (self.rect.height / 2) - (text_rect.height / 2)

        self.surf.fill("#999999")
        self.surf.blit(self.text, (text_x, text_y))
        

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
