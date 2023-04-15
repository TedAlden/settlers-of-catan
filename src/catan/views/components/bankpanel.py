import pygame

pygame.font.init()
EIGHT_BIT_FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)


class BankPanel(pygame.sprite.Sprite):

    def __init__(self, bank, top_left):
        self.bank = bank
        self.topleft = top_left
        self.font = EIGHT_BIT_FONT
        
        self.surf = pygame.Surface((300, 220))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left   

    
    def draw(self, screen):
        self.surf.fill("#999999")
        b = self.bank
        self.surf.blit(self.font.render("Bank", True, "gold"), (10, 10))
        self.surf.blit(self.font.render(f"Lumber: {b.count_lumber()}", True, "white"), (10, 40))
        self.surf.blit(self.font.render(f"Wool: {b.count_wool()}", True, "white"), (10, 70))
        self.surf.blit(self.font.render(f"Grain: {b.count_grain()}", True, "white"), (10, 100))
        self.surf.blit(self.font.render(f"Brick: {b.count_brick()}", True, "white"), (10, 130))
        self.surf.blit(self.font.render(f"Ore: {b.count_ore()}", True, "white"), (10, 160))
        self.surf.blit(self.font.render(f"Development cards: {b.count_development_cards()}", True, "white"), (10, 190))

        screen.blit(self.surf, self.rect)
