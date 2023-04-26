import pygame

from catan.util.pathresolver import resolve_path
from catan.views.components.button import Button

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)
TITLE_FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 54)

WATER = pygame.image.load(resolve_path("catan/assets/images/water.png"))


# TODO: check if player has access to harbours for bank trades


class BankTradeView:

    def __init__(self, app):
        self.app = app

        self.init()

        # choose how much lumber to send
        self.btn_decr_lumber_send = Button("<", (365, 240), size=(40, 50))
        txt = self.__format_resource_text(self.amt_lumber_send, self.amt_lumber_send_max)
        self.txt_lumber_send = Button(txt, (415, 240), size=(100, 50))
        self.btn_incr_lumber_send = Button(">", (525, 240), size=(40, 50))

        # choose how much wool to send
        self.btn_decr_wool_send = Button("<", (365, 300), size=(40, 50))
        txt = self.__format_resource_text(self.amt_wool_send, self.amt_wool_send_max)
        self.txt_wool_send = Button(txt, (415, 300), size=(100, 50))
        self.btn_incr_wool_send = Button(">", (525, 300), size=(40, 50))

        # choose how much grain to send
        self.btn_decr_grain_send = Button("<", (365, 360), size=(40, 50))
        txt = self.__format_resource_text(self.amt_grain_send, self.amt_grain_send_max)
        self.txt_grain_send = Button(txt, (415, 360), size=(100, 50))
        self.btn_incr_grain_send = Button(">", (525, 360), size=(40, 50))

        # choose how much brick to send
        self.btn_decr_brick_send = Button("<", (365, 420), size=(40, 50))
        txt = self.__format_resource_text(self.amt_brick_send, self.amt_brick_send_max)
        self.txt_brick_send = Button(txt, (415, 420), size=(100, 50))
        self.btn_incr_brick_send = Button(">", (525, 420), size=(40, 50))

        # choose how much ore to send
        self.btn_decr_ore_send = Button("<", (365, 480), size=(40, 50))
        txt = self.__format_resource_text(self.amt_ore_send, self.amt_ore_send_max)
        self.txt_ore_send = Button(txt, (415, 480), size=(100, 50))
        self.btn_incr_ore_send = Button(">", (525, 480), size=(40, 50))

        # choose what to get in return for lumber trade
        self.btn_decr_res_1 = Button("<", (705, 240), size=(40, 50))
        txt = "10 Lumber"
        self.txt_res_1 = Button(txt, (755, 240), size=(150, 50))
        self.btn_incr_res_1 = Button(">", (915, 240), size=(40, 50))

        # choose what to get in return for wool trade
        self.btn_decr_res_2 = Button("<", (705, 300), size=(40, 50))
        txt = "10 Lumber"
        self.txt_res_2 = Button(txt, (755, 300), size=(150, 50))
        self.btn_incr_res_2 = Button(">", (915, 300), size=(40, 50))

        # choose what to get in return for grain trade
        self.btn_decr_res_3 = Button("<", (705, 360), size=(40, 50))
        txt = "10 Lumber"
        self.txt_res_3 = Button(txt, (755, 360), size=(150, 50))
        self.btn_incr_res_3 = Button(">", (915, 360), size=(40, 50))

        # choose what to get in return for brick trade
        self.btn_decr_res_4 = Button("<", (705, 420), size=(40, 50))
        txt = "10 Lumber"
        self.txt_res_4 = Button(txt, (755, 420), size=(150, 50))
        self.btn_incr_res_4 = Button(">", (915, 420), size=(40, 50))

        # choose what to get in return for ore trade
        self.btn_decr_res_5 = Button("<", (705, 480), size=(40, 50))
        txt = "10 Lumber"
        self.txt_res_5 = Button(txt, (755, 480), size=(150, 50))
        self.btn_incr_res_5 = Button(">", (915, 480), size=(40, 50))


        self.btn_back = Button("Cancel", (10, 10))
        self.btn_make_trade = Button("Make trade", (530, 700))


    def init(self):
        self.trade_sender = self.app.game_controller.get_current_player()
        self.bank = self.app.game_controller.get_bank()

        # how many resources to be sent
        self.amt_lumber_send = 0
        self.amt_wool_send = 0
        self.amt_grain_send = 0
        self.amt_brick_send = 0
        self.amt_ore_send = 0

        # the maximum amount of each resource the trading player owns
        self.amt_lumber_send_max = self.trade_sender.count_lumber()
        self.amt_wool_send_max = self.trade_sender.count_wool()
        self.amt_grain_send_max = self.trade_sender.count_grain()
        self.amt_brick_send_max = self.trade_sender.count_brick()
        self.amt_ore_send_max = self.trade_sender.count_ore()

        # how many resources to be received
        self.amt_lumber_receive = 0
        self.amt_wool_receive = 0
        self.amt_grain_receive = 0
        self.amt_brick_receive = 0
        self.amt_ore_receive = 0


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.btn_back.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.game_view)

                # adjusting how much lumber to send
                if self.btn_decr_lumber_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_lumber_send - 1, 0)
                    self.amt_lumber_send = amt
                    txt = self.__format_resource_text(amt, self.amt_lumber_send_max)
                    self.txt_lumber_send.set_text(txt)

                if self.btn_incr_lumber_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_lumber_send + 1, self.amt_lumber_send_max)
                    self.amt_lumber_send = amt
                    txt = self.__format_resource_text(amt, self.amt_lumber_send_max)
                    self.txt_lumber_send.set_text(txt)

                # adjusting how much wool to send
                if self.btn_decr_wool_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_wool_send - 1, 0)
                    self.amt_wool_send = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_send_max)
                    self.txt_wool_send.set_text(txt)

                if self.btn_incr_wool_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_wool_send + 1, self.amt_wool_send_max)
                    self.amt_wool_send = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_send_max)
                    self.txt_wool_send.set_text(txt)

                # adjusting how much grain to send
                if self.btn_decr_grain_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_grain_send - 1, 0)
                    self.amt_grain_send = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_send_max)
                    self.txt_grain_send.set_text(txt)

                if self.btn_incr_grain_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_grain_send + 1, self.amt_grain_send_max)
                    self.amt_grain_send = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_send_max)
                    self.txt_grain_send.set_text(txt)

                # adjusting how much brick to send
                if self.btn_decr_brick_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_brick_send - 1, 0)
                    self.amt_brick_send = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_send_max)
                    self.txt_brick_send.set_text(txt)

                if self.btn_incr_brick_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_brick_send + 1, self.amt_brick_send_max)
                    self.amt_brick_send = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_send_max)
                    self.txt_brick_send.set_text(txt)

                # adjusting how much ore to send
                if self.btn_decr_ore_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_ore_send - 1, 0)
                    self.amt_ore_send = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_send_max)
                    self.txt_ore_send.set_text(txt)

                if self.btn_incr_ore_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_ore_send + 1, self.amt_ore_send_max)
                    self.amt_ore_send = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_send_max)
                    self.txt_ore_send.set_text(txt)


    def on_update(self):
        pass


    def on_render(self, screen):
        # screen.fill("black")
        screen.blit(WATER, (0, 0))

        title = TITLE_FONT.render("Bank Trading", True, "white")
        width, _ = title.get_rect().size
        screen.blit(title, (640 - width / 2, 50))

        sender = self.trade_sender.name
        screen.blit(FONT.render(f"{sender}'s resources", True, "white"), (365, 200))

        screen.blit(FONT.render("Lumber", True, "white"), (200, 255))
        screen.blit(FONT.render("Wool", True, "white"), (200, 315))
        screen.blit(FONT.render("Grain", True, "white"), (200, 375))
        screen.blit(FONT.render("Brick", True, "white"), (200, 435))
        screen.blit(FONT.render("Ore", True, "white"), (200, 495))

        self.btn_decr_lumber_send.draw(screen)
        self.txt_lumber_send.draw(screen)
        self.btn_incr_lumber_send.draw(screen)

        self.btn_decr_wool_send.draw(screen)
        self.txt_wool_send.draw(screen)
        self.btn_incr_wool_send.draw(screen)

        self.btn_decr_grain_send.draw(screen)
        self.txt_grain_send.draw(screen)
        self.btn_incr_grain_send.draw(screen)

        self.btn_decr_brick_send.draw(screen)
        self.txt_brick_send.draw(screen)
        self.btn_incr_brick_send.draw(screen)

        self.btn_decr_ore_send.draw(screen)
        self.txt_ore_send.draw(screen)
        self.btn_incr_ore_send.draw(screen)

        screen.blit(FONT.render(f"Banks's resources", True, "white"), (705, 200))

        self.btn_decr_res_1.draw(screen)
        self.txt_res_1.draw(screen)
        self.btn_incr_res_1.draw(screen)

        self.btn_decr_res_2.draw(screen)
        self.txt_res_2.draw(screen)
        self.btn_incr_res_2.draw(screen)

        self.btn_decr_res_3.draw(screen)
        self.txt_res_3.draw(screen)
        self.btn_incr_res_3.draw(screen)

        self.btn_decr_res_4.draw(screen)
        self.txt_res_4.draw(screen)
        self.btn_incr_res_4.draw(screen)

        self.btn_decr_res_5.draw(screen)
        self.txt_res_5.draw(screen)
        self.btn_incr_res_5.draw(screen)

        self.btn_back.draw(screen)
        self.btn_make_trade.draw(screen)


    def __format_resource_text(self, amount, maximum):
        return f"{amount} / {maximum}"