import pygame

from catan.type import ResourceType


class Harbour:
    
    def __init__(self, axial_coord, resource_type, node1, node2):
        self.axial_coord = axial_coord
        self.resource_type = resource_type
        self.settlements = [node1, node2]
        self.trade_ratio = 2  # 2:1

        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()

        if resource_type == ResourceType.ANY:
            self.trade_ratio = 3  # 3:1


    def get_type(self):
        return self.resource_type
    

    def get_trade_ratio(self):
        return self.trade_ratio
    

    def get_settlements(self):
        return self.settlements


    def set_pos(self, center_x, center_y):
        self.rect.center = (center_x, center_y)


    def get_pos(self):
        return self.rect.center
