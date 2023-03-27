import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left_x, top_left_y, colour, background, font):
        self.text = text
        self.colour = colour
        self.background = background
        self.font = font
        self.surf = self.font.render(self.text, True, self.colour, self.background)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (top_left_x, top_left_y)


    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class TextBox(pygame.sprite.Sprite):

    def __init__(self, text_generator, top_left_x, top_left_y, colour, background, font):
        self.topleft = top_left_x, top_left_y
        self.colour = colour
        self.background = background
        self.font = font
        self.text_generator = text_generator
        self.text = str(self.text_generator())
        self.surf = self.font.render(self.text, True, self.colour, self.background)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (top_left_x, top_left_y)


    def update(self):
        self.text = str(self.text_generator())

    
    def draw(self, screen):
        self.surf = self.font.render(self.text, True, self.colour, self.background)
        self.rect = self.surf.get_rect()
        self.rect.topleft = self.topleft
        screen.blit(self.surf, self.rect)