import pygame

from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)

RES_CARD = pygame.image.load(resolve_path("catan/assets/images/res_card_back.png"))
DEV_CARD = pygame.image.load(resolve_path("catan/assets/images/dev_card_back.png"))
VP_ICON = pygame.image.load(resolve_path("catan/assets/images/vp_icon.png"))
ARMY = pygame.image.load(resolve_path("catan/assets/images/largest_army.png"))
ROAD = pygame.image.load(resolve_path("catan/assets/images/longest_road.png"))


class PlayerPanel(pygame.sprite.Sprite):

    def __init__(self, player, top_left):
        self.player = player
        self.topleft = top_left
        self.font = FONT
        
        self.surf = pygame.Surface((300, 148))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left


    def update(self):
        self.name = self.player.name
        self.colour = self.player.colour
        self.vp = self.player.count_vp()
        self.road = self.player.count_longest_road()
        self.army = self.player.count_army()
        self.res = self.player.count_resource_cards()
        self.dev = self.player.count_development_cards()

    
    def draw(self, screen):
        self.surf.fill("#999999")

        pygame.draw.circle(self.surf, self.colour, (19, 19), 9)
        self.surf.blit(self.font.render(self.name, True, self.colour), (38, 10))

        self.surf.blit(RES_CARD, (10, 40))
        self.surf.blit(DEV_CARD, (58, 40))
        self.surf.blit(VP_ICON, (106, 40))

        # FIXME: only show if player has longest road...
        self.surf.blit(ROAD, (160, 24))

        # FIXME: only show if player has largest army...
        self.surf.blit(ARMY, (230, 24))

        self.surf.blit(self.font.render(str(self.res), True, "white"), (24, 108))
        self.surf.blit(self.font.render(str(self.dev), True, "white"), (72, 108))
        self.surf.blit(self.font.render(str(self.vp), True, "white"), (120, 108))

        screen.blit(self.surf, self.rect)
