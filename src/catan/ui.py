import pygame
import random

from catan.shapes import draw_dice

DEFAULT_FONT = pygame.font.SysFont(None, 32)
EIGHT_BIT_FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)


class Button(pygame.sprite.Sprite):

    def __init__(self, text, top_left, font, colour="white", background=None):
        self.text = text
        self.colour = colour
        self.background = background
        self.font = font

        self.enabled = True
        # TODO: enable/disable buttons depending on what turn is taken

        self.surf = pygame.Surface((220, 50))
        self.surf.fill("#999999")
        self.rect = self.surf.get_rect()
        self.rect.topleft = top_left
    
        self.text = self.font.render(self.text, True, self.colour, self.background)
        text_rect = self.text.get_rect()
        text_x = (self.rect.width / 2) - (text_rect.width / 2)
        text_y = (self.rect.height / 2) - (text_rect.height / 2)
        self.surf.blit(self.text, (text_x, text_y))
        

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        

class Dice(pygame.sprite.Sprite):

    def __init__(self, topleft):
        self.value = 6
        self.surf = pygame.Surface((64, 64))
        self.rect = self.surf.get_rect()
        self.rect.topleft = topleft


    def roll(self):
        self.value = random.randint(1, 6)


    def draw(self, screen):
        draw_dice(screen, self.rect.topleft, self.value)


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
