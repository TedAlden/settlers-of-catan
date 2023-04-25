import pygame

from catan.views.components.button import Button
from catan.util.pathresolver import resolve_path

WATER = pygame.image.load(resolve_path("catan/assets/images/water.png"))
TITLE_FONT_SMALL = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 48)
TITLE_FONT_LARGE = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 96)

class MenuView:

    def __init__(self, app):
        self.app = app
        self.btn_new = Button("New game", (300, 600))
        self.btn_load = Button("Load game", (530, 600))
        self.btn_exit = Button("Exit", (760, 600))


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # clicking on left hand side UI buttons...
                if self.btn_new.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.new_game_view)

                if self.btn_load.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.load_game_view)

                if self.btn_exit.rect.collidepoint(mouse_pos):
                    self.app.running = False


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.fill("black")
        screen.blit(WATER, (0, 0))

        title_1 = TITLE_FONT_SMALL.render("Settlers of", True, "white")
        width = title_1.get_rect().width
        screen.blit(title_1, (640 - width / 2, 220))

        title_2 = TITLE_FONT_LARGE.render("Catan", True, "white")
        width = title_2.get_rect().width
        screen.blit(title_2, (640 - width / 2, 300))

        self.btn_new.draw(screen)
        self.btn_load.draw(screen)
        self.btn_exit.draw(screen)
