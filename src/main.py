import pygame
import pathlib
from catan.gameview import GameView


SCREEN_FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Settlers of Catan"
ICON_PATH = pathlib.Path(__file__).parent.parent.joinpath("icon.png")


class Catan:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()
        self._running = True
        self.game_view = GameView()
        self.current_view = self.game_view


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.current_view.on_event(event)


    def on_update(self):
        self.current_view.on_update()
        self.clock.tick(30)


    def on_render(self):
        self.current_view.on_render(self.screen)
        
        pygame.display.flip()


    def on_execute(self):
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
            self.on_render()
        self.on_cleanup()


    def on_cleanup(self):
        pygame.quit()


if __name__ == "__main__":
    c = Catan()
    c.on_execute()
