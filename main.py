import pygame
from board import Board

pygame.init()

screen = pygame.display.set_mode([500, 500])

b = Board(50, 45)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    b.draw(screen)

    pygame.display.flip()

pygame.quit()
