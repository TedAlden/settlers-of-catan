import pygame
from board import Board


SCREEN_FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Settlers of Catan"


class Catan:

    def __init__(self):
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board(50, 45)
        self.running = True

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.clock.tick(30)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        pygame.display.flip()


def main():
    pygame.init()
    c = Catan()

    while c.running:
        c.update()
        c.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
