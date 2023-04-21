import pygame

from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)


class TextInput(pygame.sprite.Sprite):

    def __init__(self, top_left, colour="white", size=(220, 50)):
        self.input_text = ""
        self.colour = colour
        self.font = FONT
        self.selected = False

        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left


    def on_event(self, event):
        if self.selected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        

    def draw(self, screen):
        self.surf.fill("#999999")

        text = self.font.render(self.input_text, True, self.colour)
        text_rect = text.get_rect()
        text_x = (self.rect.width / 2) - (text_rect.width / 2)
        text_y = (self.rect.height / 2) - (text_rect.height / 2)

        
        if self.selected:
            pygame.draw.rect(self.surf, "gold", (0,0,*self.rect.size), width=2)

        self.surf.blit(text, (text_x, text_y))
        screen.blit(self.surf, self.rect)
