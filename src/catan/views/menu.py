import pygame

from catan.views.components.button import Button
from catan.util.pathresolver import resolve_path

BACKGROUND_IMAGE = pygame.image.load(resolve_path("catan/assets/images/main_menu_background.png"))


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
        # screen.blit(BACKGROUND_IMAGE, (0, 0))

        self.btn_new.draw(screen)
        self.btn_load.draw(screen)
        self.btn_exit.draw(screen)
