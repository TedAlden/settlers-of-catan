import pygame

from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left, colour="white", size=(220, 50)):
        self.text = text
        self.colour = colour
        self.font = FONT
        self.selected = False

        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left
    
        self.text_surf = self.font.render(self.text, True, self.colour)
        text_rect = self.text_surf.get_rect()
        self.text_x = (self.rect.width / 2) - (text_rect.width / 2)
        self.text_y = (self.rect.height / 2) - (text_rect.height / 2)


    def on_event(self, event):
        pass


    def set_text(self, text):
        self.text = text
        self.text_surf = self.font.render(self.text, True, self.colour)
        text_rect = self.text.get_rect()
        self.text_x = (self.rect.width / 2) - (text_rect.width / 2)
        self.text_y = (self.rect.height / 2) - (text_rect.height / 2)
        

    def draw(self, screen):
        self.surf.fill("#999999")
        if self.selected:
            pygame.draw.rect(self.surf, "gold", (0,0,*self.rect.size), width=3)
        self.surf.blit(self.text_surf, (self.text_x, self.text_y))
        screen.blit(self.surf, self.rect)
