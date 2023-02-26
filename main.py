import pygame
from board import Board


SCREEN_FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Settlers of Catan"


class Catan:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board(50)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_update(self):
        self.clock.tick(30)

    def on_render(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
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
