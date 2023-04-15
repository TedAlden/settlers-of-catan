import pygame

FONT_PATH = "src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf"
# FONT_PATH = "src\\catan\\assets\\fonts\\WashingtonText.ttf"


class BankPanel(pygame.sprite.Sprite):

    def __init__(self, bank, top_left):
        self.bank = bank
        self.topleft = top_left
        self.font = pygame.font.Font(FONT_PATH, 18)
        
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

        pygame.draw.rect(self.surf, "#e6d85e", (10, 40, 40, 60))
        pygame.draw.rect(self.surf, "#5fc73a", (58, 40, 40, 60))
        pygame.draw.rect(self.surf, "#168a35", (106, 40, 40, 60))
        pygame.draw.rect(self.surf, "#e09e2b", (154, 40, 40, 60))
        pygame.draw.rect(self.surf, "#8c8c8c", (202, 40, 40, 60))
        pygame.draw.rect(self.surf, "purple", (250, 40, 40, 60))

        self.surf.blit(self.font.render(str(self.lumber), True, "white"), (24, 108))
        self.surf.blit(self.font.render(str(self.wool), True, "white"), (72, 108))
        self.surf.blit(self.font.render(str(self.grain), True, "white"), (120, 108))
        self.surf.blit(self.font.render(str(self.brick), True, "white"), (168, 108))
        self.surf.blit(self.font.render(str(self.ore), True, "white"), (216, 108))
        self.surf.blit(self.font.render(str(self.devs), True, "white"), (264, 108))

        screen.blit(self.surf, self.rect)
