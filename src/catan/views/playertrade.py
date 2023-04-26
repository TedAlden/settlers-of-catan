import pygame

from catan.util.pathresolver import resolve_path
from catan.views.components.button import Button

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)
TITLE_FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 54)

WATER = pygame.image.load(resolve_path("catan/assets/images/water.png"))


class PlayerTradeView:

    def __init__(self, app):
        self.app = app

        self.init()

        # choose player to trade with
        self.btn_decr_player = Button("<", (480, 200), size=(40, 50))
        self.txt_player = Button(self.trade_other.name, (540, 200), size=(200, 50))
        self.btn_incr_player = Button(">", (750, 200), size=(40, 50))

        # choose how much lumber to send
        self.btn_decr_lumber_send = Button("<", (365, 340), size=(40, 50))
        txt = self.__format_resource_text(self.amt_lumber_send, self.amt_lumber_send_max)
        self.txt_lumber_send = Button(txt, (415, 340), size=(100, 50))
        self.btn_incr_lumber_send = Button(">", (525, 340), size=(40, 50))

        # choose how much wool to send
        self.btn_decr_wool_send = Button("<", (365, 400), size=(40, 50))
        txt = self.__format_resource_text(self.amt_wool_send, self.amt_wool_send_max)
        self.txt_wool_send = Button(txt, (415, 400), size=(100, 50))
        self.btn_incr_wool_send = Button(">", (525, 400), size=(40, 50))

        # choose how much grain to send
        self.btn_decr_grain_send = Button("<", (365, 460), size=(40, 50))
        txt = self.__format_resource_text(self.amt_grain_send, self.amt_grain_send_max)
        self.txt_grain_send = Button(txt, (415, 460), size=(100, 50))
        self.btn_incr_grain_send = Button(">", (525, 460), size=(40, 50))

        # choose how much brick to send
        self.btn_decr_brick_send = Button("<", (365, 520), size=(40, 50))
        txt = self.__format_resource_text(self.amt_brick_send, self.amt_brick_send_max)
        self.txt_brick_send = Button(txt, (415, 520), size=(100, 50))
        self.btn_incr_brick_send = Button(">", (525, 520), size=(40, 50))

        # choose how much ore to send
        self.btn_decr_ore_send = Button("<", (365, 580), size=(40, 50))
        txt = self.__format_resource_text(self.amt_ore_send, self.amt_ore_send_max)
        self.txt_ore_send = Button(txt, (415, 580), size=(100, 50))
        self.btn_incr_ore_send = Button(">", (525, 580), size=(40, 50))

        # choose how much lumber to receive
        self.btn_decr_lumber_receive = Button("<", (705, 340), size=(40, 50))
        txt = self.__format_resource_text(self.amt_lumber_receive, self.amt_lumber_receive_max)
        self.txt_lumber_receive = Button(txt, (755, 340), size=(100, 50))
        self.btn_incr_lumber_receive = Button(">", (865, 340), size=(40, 50))

        # choose how much wool to receive
        self.btn_decr_wool_receive = Button("<", (705, 400), size=(40, 50))
        txt = self.__format_resource_text(self.amt_wool_receive, self.amt_wool_receive_max)
        self.txt_wool_receive = Button(txt, (755, 400), size=(100, 50))
        self.btn_incr_wool_receive = Button(">", (865, 400), size=(40, 50))

        # choose how much grain to receive
        self.btn_decr_grain_receive = Button("<", (705, 460), size=(40, 50))
        txt = self.__format_resource_text(self.amt_grain_receive, self.amt_grain_receive_max)
        self.txt_grain_receive = Button(txt, (755, 460), size=(100, 50))
        self.btn_incr_grain_receive = Button(">", (865, 460), size=(40, 50))

        # choose how much brick to receive
        self.btn_decr_brick_receive = Button("<", (705, 520), size=(40, 50))
        txt = self.__format_resource_text(self.amt_brick_receive, self.amt_brick_receive_max)
        self.txt_brick_receive = Button(txt, (755, 520), size=(100, 50))
        self.btn_incr_brick_receive = Button(">", (865, 520), size=(40, 50))

        # choose how much ore to receive
        self.btn_decr_ore_receive = Button("<", (705, 580), size=(40, 50))
        txt = self.__format_resource_text(self.amt_ore_receive, self.amt_ore_receive_max)
        self.txt_ore_receive = Button(txt, (755, 580), size=(100, 50))
        self.btn_incr_ore_receive = Button(">", (865, 580), size=(40, 50))


        self.btn_back = Button("Cancel", (10, 10))
        self.btn_make_trade = Button("Make trade", (530, 700))

    
    def init(self):
        self.trade_sender = self.app.game_controller.get_current_player()
        self.players = self.app.game_controller.get_players()

        self.other_players = self.players.copy()
        self.other_players.remove(self.trade_sender)

        self.trade_other = self.other_players[0]

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

        # the maximum amount of each resource the other player owns
        self.amt_lumber_receive_max = self.trade_other.count_lumber()
        self.amt_wool_receive_max = self.trade_other.count_wool()
        self.amt_grain_receive_max = self.trade_other.count_grain()
        self.amt_brick_receive_max = self.trade_other.count_brick()
        self.amt_ore_receive_max = self.trade_other.count_ore()

    
    def __make_trade(self):
        print(self.amt_lumber_receive)
        print(self.amt_wool_receive)
        print(self.amt_grain_receive)
        print(self.amt_brick_receive)
        print(self.amt_ore_receive)

        # send resources from the trade initiator to the receiver
        self.trade_sender.add_resources(lumber = self.amt_lumber_receive,
                                        wool = self.amt_wool_receive,
                                        grain = self.amt_grain_receive,
                                        brick = self.amt_brick_receive,
                                        ore = self.amt_ore_receive)
        
        self.trade_other.remove_resources(lumber = self.amt_lumber_receive,
                                          wool = self.amt_wool_receive,
                                          grain = self.amt_grain_receive,
                                          brick = self.amt_brick_receive,
                                          ore = self.amt_ore_receive)
        
        # send the exchanged resources back to the trade initiator
        self.trade_sender.remove_resources(lumber = self.amt_lumber_send,
                                           wool = self.amt_wool_send,
                                           grain = self.amt_grain_send,
                                           brick = self.amt_brick_send,
                                           ore = self.amt_ore_send)
        
        self.trade_other.add_resources(lumber = self.amt_lumber_send,
                                       wool = self.amt_wool_send,
                                       grain = self.amt_grain_send,
                                       brick = self.amt_brick_send,
                                       ore = self.amt_ore_send)


    def __format_resource_text(self, amount, maximum):
        return f"{amount} / {maximum}"
    

    def __reset_trade_receiver_resources(self):
        # reset the chosen amount of resources to receive in the trade,
        # when changing the player that is being traded with, since they
        # will likely have a different amount of resources.
        self.amt_lumber_receive = 0
        self.amt_wool_receive = 0
        self.amt_grain_receive = 0
        self.amt_brick_receive = 0
        self.amt_ore_receive = 0

        self.amt_lumber_receive_max = self.trade_other.count_lumber()
        self.amt_wool_receive_max = self.trade_other.count_wool()
        self.amt_grain_receive_max = self.trade_other.count_grain()
        self.amt_brick_receive_max = self.trade_other.count_brick()
        self.amt_ore_receive_max = self.trade_other.count_ore()

        lumber_text = self.__format_resource_text(self.amt_lumber_receive, self.amt_lumber_receive_max)
        self.txt_lumber_receive.set_text(lumber_text)

        wool_text = self.__format_resource_text(self.amt_wool_receive, self.amt_wool_receive_max)
        self.txt_wool_receive.set_text(wool_text)

        grain_text = self.__format_resource_text(self.amt_grain_receive, self.amt_grain_receive_max)
        self.txt_grain_receive.set_text(grain_text)

        brick_text = self.__format_resource_text(self.amt_brick_receive, self.amt_brick_receive_max)
        self.txt_brick_receive.set_text(brick_text)

        ore_text = self.__format_resource_text(self.amt_ore_receive, self.amt_ore_receive_max)
        self.txt_ore_receive.set_text(ore_text)


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.btn_back.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.game_view)

                # choosing which player to trade with
                if self.btn_decr_player.rect.collidepoint(mouse_pos):
                    idx = self.other_players.index(self.trade_other)
                    idx = (idx - 1) % len(self.other_players)
                    self.trade_other = self.other_players[idx]
                    self.txt_player.set_text(self.trade_other.name)
                    self.__reset_trade_receiver_resources()

                if self.btn_incr_player.rect.collidepoint(mouse_pos):
                    idx = self.other_players.index(self.trade_other)
                    idx = (idx + 1) % len(self.other_players)
                    self.trade_other = self.other_players[idx]
                    self.txt_player.set_text(self.trade_other.name)
                    self.__reset_trade_receiver_resources()

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

                # adjusting how much lumber to receive
                if self.btn_decr_lumber_receive.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_lumber_receive - 1, 0)
                    self.amt_lumber_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_lumber_receive_max)
                    self.txt_lumber_receive.set_text(txt)

                if self.btn_incr_lumber_receive.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_lumber_receive + 1, self.amt_lumber_receive_max)
                    self.amt_lumber_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_lumber_receive_max)
                    self.txt_lumber_receive.set_text(txt)

                # adjusting how much wool to receive
                if self.btn_decr_wool_receive.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_wool_receive - 1, 0)
                    self.amt_wool_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_receive_max)
                    self.txt_wool_receive.set_text(txt)

                if self.btn_incr_wool_receive.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_wool_receive + 1, self.amt_wool_receive_max)
                    self.amt_wool_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_receive_max)
                    self.txt_wool_receive.set_text(txt)

                # adjusting how much grain to receive
                if self.btn_decr_grain_receive.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_grain_receive - 1, 0)
                    self.amt_grain_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_receive_max)
                    self.txt_grain_receive.set_text(txt)

                if self.btn_incr_grain_receive.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_grain_receive + 1, self.amt_grain_receive_max)
                    self.amt_grain_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_receive_max)
                    self.txt_grain_receive.set_text(txt)

                # adjusting how much brick to receive
                if self.btn_decr_brick_receive.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_brick_receive - 1, 0)
                    self.amt_brick_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_receive_max)
                    self.txt_brick_receive.set_text(txt)

                if self.btn_incr_brick_receive.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_brick_receive + 1, self.amt_brick_receive_max)
                    self.amt_brick_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_receive_max)
                    self.txt_brick_receive.set_text(txt)

                # adjusting how much ore to receive
                if self.btn_decr_ore_receive.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_ore_receive - 1, 0)
                    self.amt_ore_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_receive_max)
                    self.txt_ore_receive.set_text(txt)

                if self.btn_incr_ore_receive.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_ore_receive + 1, self.amt_ore_receive_max)
                    self.amt_ore_receive = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_receive_max)
                    self.txt_ore_receive.set_text(txt)

                # make trade
                if self.btn_make_trade.rect.collidepoint(mouse_pos):
                    self.__make_trade()
                    self.app.set_view(self.app.game_view)


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.blit(WATER, (0, 0))

        title = TITLE_FONT.render("Player Trading", True, "white")
        width, _ = title.get_rect().size
        screen.blit(title, (640 - width / 2, 50))

        screen.blit(FONT.render("Trade with player:", True, "white"), (200, 215))

        self.btn_decr_player.draw(screen)
        self.txt_player.draw(screen)
        self.btn_incr_player.draw(screen)

        sender = self.trade_sender.name
        screen.blit(FONT.render(f"{sender}'s resources", True, "white"), (365, 300))

        screen.blit(FONT.render("Lumber", True, "white"), (200, 355))
        screen.blit(FONT.render("Wool", True, "white"), (200, 415))
        screen.blit(FONT.render("Grain", True, "white"), (200, 475))
        screen.blit(FONT.render("Brick", True, "white"), (200, 535))
        screen.blit(FONT.render("Ore", True, "white"), (200, 595))

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

        receiver = self.trade_other.name
        screen.blit(FONT.render(f"{receiver}'s resources", True, "white"), (705, 300))

        self.btn_decr_lumber_receive.draw(screen)
        self.txt_lumber_receive.draw(screen)
        self.btn_incr_lumber_receive.draw(screen)

        self.btn_decr_wool_receive.draw(screen)
        self.txt_wool_receive.draw(screen)
        self.btn_incr_wool_receive.draw(screen)

        self.btn_decr_grain_receive.draw(screen)
        self.txt_grain_receive.draw(screen)
        self.btn_incr_grain_receive.draw(screen)

        self.btn_decr_brick_receive.draw(screen)
        self.txt_brick_receive.draw(screen)
        self.btn_incr_brick_receive.draw(screen)

        self.btn_decr_ore_receive.draw(screen)
        self.txt_ore_receive.draw(screen)
        self.btn_incr_ore_receive.draw(screen)

        self.btn_back.draw(screen)
        self.btn_make_trade.draw(screen)
