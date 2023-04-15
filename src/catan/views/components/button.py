import pygame

EIGHT_BIT_FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left, font, colour="white", background=None):
        self.text = text
        self.colour = colour
        self.background = background
        self.font = font

        self.enabled = True
        # TODO: enable/disable buttons depending on what turn is taken

        self.surf = pygame.Surface((220, 50))
        self.surf.fill("#999999")
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left
    
        self.text = self.font.render(self.text, True, self.colour, self.background)
        text_rect = self.text.get_rect()
        text_x = (self.rect.width / 2) - (text_rect.width / 2)
        text_y = (self.rect.height / 2) - (text_rect.height / 2)
        self.surf.blit(self.text, (text_x, text_y))
        

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
