import pygame

pygame.font.init()
BUTTON_FONT = pygame.font.SysFont(None, 32)


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left_x, top_left_y):
        self.text = text
        self.surf = BUTTON_FONT.render(self.text, True, "white", "black")
        self.rect = self.surf.get_rect()
        self.rect.topleft = (top_left_x, top_left_y)


    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class TextBox(pygame.sprite.Sprite):

    def __init__(self, text_generator, top_left_x, top_left_y):
        self.topleft = top_left_x, top_left_y
        self.text_generator = text_generator
        self.text = str(self.text_generator())
        self.surf = BUTTON_FONT.render(self.text, True, "white", "#444444")
        self.rect = self.surf.get_rect()
        self.rect.topleft = (top_left_x, top_left_y)


    def update(self):
        self.text = str(self.text_generator())

    
    def draw(self, screen):
        self.surf = BUTTON_FONT.render(self.text, True, "white", "#444444")
        self.rect = self.surf.get_rect()
        self.rect.topleft = self.topleft
        screen.blit(self.surf, self.rect)