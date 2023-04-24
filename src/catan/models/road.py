import pygame


class Road(pygame.sprite.Sprite):

    def __init__(self, node1, node2, owner):
        self.settlements = [node1, node2]
        self.owner = owner
