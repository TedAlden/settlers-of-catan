import pygame

EIGHT_BIT_FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)


class PlayerPanel(pygame.sprite.Sprite):

    def __init__(self, player, top_left):
        self.player = player
        self.topleft = top_left
        self.font = EIGHT_BIT_FONT
        
        self.surf = pygame.Surface((300, 130))
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left   

    
    def draw(self, screen):
        self.surf.fill("#999999")
        p = self.player
        self.surf.blit(self.font.render(p.name, True, p.colour), (10, 10))
        self.surf.blit(self.font.render(f"VPs: {p.count_vp()}", True, "white"), (215, 10))

        self.surf.blit(self.font.render(f"Longest road: {p.count_longest_road()}", True, "white"), (10, 40))
        self.surf.blit(self.font.render(f"Army: {p.count_army()}", True, "white"), (205, 40))

        self.surf.blit(self.font.render(f"Resource cards: {p.count_resource_cards()}", True, "white"), (10, 70))
        self.surf.blit(self.font.render(f"Development cards: {p.count_development_cards()}", True, "white"), (10, 100))

        screen.blit(self.surf, self.rect)
