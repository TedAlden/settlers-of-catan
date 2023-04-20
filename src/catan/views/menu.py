import pygame

from catan.views.components.button import Button


class MenuView:

    def __init__(self, app):
        self.app = app
        self.btn_new = Button("New game", (200, 200))
        self.btn_load = Button("Load game", (200, 300))
        self.btn_exit = Button("Exit", (200, 400))


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # clicking on left hand side UI buttons...
                if self.btn_new.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.game_view)

                if self.btn_load.rect.collidepoint(mouse_pos):
                    pass

                if self.btn_exit.rect.collidepoint(mouse_pos):
                    self.app.running = False


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.fill("black")

        self.btn_new.draw(screen)
        self.btn_load.draw(screen)
        self.btn_exit.draw(screen)
