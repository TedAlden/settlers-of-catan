import pygame

from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)

LUMBER = pygame.image.load(resolve_path("catan/assets/images/res_card_lumber.png"))
WOOL = pygame.image.load(resolve_path("catan/assets/images/res_card_wool.png"))
GRAIN = pygame.image.load(resolve_path("catan/assets/images/res_card_grain.png"))
BRICK = pygame.image.load(resolve_path("catan/assets/images/res_card_brick.png"))
ORE = pygame.image.load(resolve_path("catan/assets/images/res_card_ore.png"))

KNIGHT = pygame.image.load(resolve_path("catan/assets/images/dev_card_knight.png"))
ROAD = pygame.image.load(resolve_path("catan/assets/images/dev_card_road.png"))
PLENTY = pygame.image.load(resolve_path("catan/assets/images/dev_card_plenty.png"))
MONOPOLY = pygame.image.load(resolve_path("catan/assets/images/dev_card_monopoly.png"))
VP = pygame.image.load(resolve_path("catan/assets/images/dev_card_knight.png"))


class InventoryPanel(pygame.sprite.Sprite):

    def __init__(self, top_left):
        self.player = None
        self.topleft = top_left
        self.font = FONT
        
        self.surf = pygame.Surface((640, 120))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left

    
    def set_player(self, player):
        self.player = player


    def update(self):
        self.lumber = self.player.count_lumber()
        self.wool = self.player.count_wool()
        self.grain = self.player.count_grain()
        self.brick = self.player.count_brick()
        self.ore = self.player.count_ore()

        self.card_knight = self.player.count_card_knight()
        self.card_road = self.player.count_card_road()
        self.card_plenty = self.player.count_card_year_plenty()
        self.card_monopoly = self.player.count_card_monopoly()
        self.card_vp = self.player.count_card_vp()


    def draw(self, screen):
        self.surf.fill("#999999")

        self.surf.blit(LUMBER, (10, 10))
        self.surf.blit(WOOL, (68, 10))
        self.surf.blit(GRAIN, (126, 10))
        self.surf.blit(BRICK, (184, 10))
        self.surf.blit(ORE, (242, 10))

        self.surf.blit(self.font.render(str(self.lumber), True, "white"), (28, 90))
        self.surf.blit(self.font.render(str(self.wool), True, "white"), (86, 90))
        self.surf.blit(self.font.render(str(self.grain), True, "white"), (144, 90))
        self.surf.blit(self.font.render(str(self.brick), True, "white"), (202, 90))
        self.surf.blit(self.font.render(str(self.ore), True, "white"), (260, 90))

        # pygame.draw.rect(self.surf, "purple", (350, 10, 48, 72))
        # pygame.draw.rect(self.surf, "purple", (408, 10, 48, 72))
        # pygame.draw.rect(self.surf, "purple", (466, 10, 48, 72))
        # pygame.draw.rect(self.surf, "purple", (524, 10, 48, 72))
        # pygame.draw.rect(self.surf, "purple", (582, 10, 48, 72))

        self.surf.blit(KNIGHT, (350, 10))
        self.surf.blit(ROAD, (408, 10))
        self.surf.blit(PLENTY, (466, 10))
        self.surf.blit(MONOPOLY, (524, 10))
        self.surf.blit(VP, (582, 10))

        self.surf.blit(self.font.render(str(self.card_knight), True, "white"), (368, 90))
        self.surf.blit(self.font.render(str(self.card_road), True, "white"), (426, 90))
        self.surf.blit(self.font.render(str(self.card_plenty), True, "white"), (484, 90))
        self.surf.blit(self.font.render(str(self.card_monopoly), True, "white"), (542, 90))
        self.surf.blit(self.font.render(str(self.card_vp), True, "white"), (600, 90))

        screen.blit(self.surf, self.rect)
