import pygame


class Road(pygame.sprite.Sprite):

    def __init__(self, node1, node2, owner):
        self.settlements = [node1, node2]
        self.owner = owner


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])
