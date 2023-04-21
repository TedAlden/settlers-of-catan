import pygame

from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)

LUMBER = pygame.image.load(resolve_path("catan/assets/images/res_card_lumber_small.png"))
WOOL = pygame.image.load(resolve_path("catan/assets/images/res_card_wool_small.png"))
GRAIN = pygame.image.load(resolve_path("catan/assets/images/res_card_grain_small.png"))
BRICK = pygame.image.load(resolve_path("catan/assets/images/res_card_brick_small.png"))
ORE = pygame.image.load(resolve_path("catan/assets/images/res_card_ore_small.png"))
DEV_CARD = pygame.image.load(resolve_path("catan/assets/images/dev_card_back.png"))


class BankPanel(pygame.sprite.Sprite):

    def __init__(self, bank, top_left):
        self.bank = bank
        self.topleft = top_left
        self.font = FONT
        
        self.surf = pygame.Surface((300, 148))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left


    def update(self):
        self.lumber = self.bank.count_lumber()
        self.wool = self.bank.count_wool()
        self.grain = self.bank.count_grain()
        self.brick = self.bank.count_brick()
        self.ore = self.bank.count_ore()
        self.devs = self.bank.count_development_cards()


    def draw(self, screen):
        self.surf.fill("#999999")

        self.surf.blit(self.font.render("Bank", True, "white"), (10, 10))

        self.surf.blit(LUMBER, (10, 40))
        self.surf.blit(WOOL, (58, 40))
        self.surf.blit(GRAIN, (106, 40))
        self.surf.blit(BRICK, (154, 40))
        self.surf.blit(ORE, (202, 40))
        self.surf.blit(DEV_CARD, (250, 40))

        self.surf.blit(self.font.render(str(self.lumber), True, "white"), (20, 108))
        self.surf.blit(self.font.render(str(self.wool), True, "white"), (68, 108))
        self.surf.blit(self.font.render(str(self.grain), True, "white"), (116, 108))
        self.surf.blit(self.font.render(str(self.brick), True, "white"), (164, 108))
        self.surf.blit(self.font.render(str(self.ore), True, "white"), (212, 108))
        self.surf.blit(self.font.render(str(self.devs), True, "white"), (260, 108))

        screen.blit(self.surf, self.rect)
