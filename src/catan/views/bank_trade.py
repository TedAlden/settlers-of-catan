import pygame
from catan.models.city import City
from catan.models.settlement import Settlement
from catan.type import ResourceType

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
        self.txt_res_1 = Button("", (755, 240), size=(150, 50))
        self.btn_incr_res_1 = Button(">", (915, 240), size=(40, 50))
        self.__update_lumber_exchange_text()

        # choose what to get in return for wool trade
        self.btn_decr_res_2 = Button("<", (705, 300), size=(40, 50))
        self.txt_res_2 = Button("", (755, 300), size=(150, 50))
        self.btn_incr_res_2 = Button(">", (915, 300), size=(40, 50))
        self.__update_wool_exchange_text()

        # choose what to get in return for grain trade
        self.btn_decr_res_3 = Button("<", (705, 360), size=(40, 50))
        self.txt_res_3 = Button("", (755, 360), size=(150, 50))
        self.btn_incr_res_3 = Button(">", (915, 360), size=(40, 50))
        self.__update_grain_exchange_text()

        # choose what to get in return for brick trade
        self.btn_decr_res_4 = Button("<", (705, 420), size=(40, 50))
        self.txt_res_4 = Button("", (755, 420), size=(150, 50))
        self.btn_incr_res_4 = Button(">", (915, 420), size=(40, 50))
        self.__update_brick_exchange_text()

        # choose what to get in return for ore trade
        self.btn_decr_res_5 = Button("<", (705, 480), size=(40, 50))
        self.txt_res_5 = Button("", (755, 480), size=(150, 50))
        self.btn_incr_res_5 = Button(">", (915, 480), size=(40, 50))
        self.__update_ore_exchange_text()

        self.btn_back = Button("Cancel", (10, 10))
        self.btn_make_trade = Button("Make trade", (530, 700))


    def __calculate_exchange(self, resource, amount):
        # calculate how much of each resource they can get with the lumber
        # i.e. 8 lumber could get - 2 wool, 2 grain, 2 ore, or 2 brick

        ratio = 4
        # TODO check if they have 3:1 any-type harbour

        # TODO check if they have 2:1 wool harbour

        # calculate how much can be gained in return, and the remainder
        # if more than necessary is being offered
        exchanged = amount // ratio

        maximum_exchange = 0

        if resource == ResourceType.WOOL:
            maximum_exchange = self.bank.count_wool()

        elif resource == ResourceType.GRAIN:
            maximum_exchange = self.bank.count_grain()

        elif resource == ResourceType.BRICK:
            maximum_exchange = self.bank.count_brick()

        elif resource == ResourceType.ORE:
            maximum_exchange = self.bank.count_ore()
            


        exchanged = min(exchanged, maximum_exchange)

        return exchanged


    def init(self):
        self.trade_sender = self.app.game_controller.get_current_player()
        self.bank = self.app.game_controller.get_bank()

        self.lumber_returns = [ResourceType.WOOL, ResourceType.GRAIN, ResourceType.BRICK, ResourceType.ORE]
        self.wool_returns = [ResourceType.LUMBER, ResourceType.GRAIN, ResourceType.BRICK, ResourceType.ORE]
        self.grain_returns = [ResourceType.LUMBER, ResourceType.WOOL, ResourceType.BRICK, ResourceType.ORE]
        self.brick_returns = [ResourceType.LUMBER, ResourceType.WOOL, ResourceType.GRAIN, ResourceType.ORE]
        self.ore_returns = [ResourceType.LUMBER, ResourceType.WOOL, ResourceType.GRAIN, ResourceType.BRICK]

        self.chosen_lumber_return = self.lumber_returns[0]
        self.chosen_wool_return = self.wool_returns[0]
        self.chosen_grain_return = self.grain_returns[0]
        self.chosen_brick_return = self.brick_returns[0]
        self.chosen_ore_return = self.ore_returns[0]

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
                    self.__update_lumber_exchange_text()

                if self.btn_incr_lumber_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_lumber_send + 1, self.amt_lumber_send_max)
                    self.amt_lumber_send = amt
                    txt = self.__format_resource_text(amt, self.amt_lumber_send_max)
                    self.txt_lumber_send.set_text(txt)
                    self.__update_lumber_exchange_text()

                # adjusting how much wool to send
                if self.btn_decr_wool_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_wool_send - 1, 0)
                    self.amt_wool_send = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_send_max)
                    self.txt_wool_send.set_text(txt)
                    self.__update_wool_exchange_text()

                if self.btn_incr_wool_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_wool_send + 1, self.amt_wool_send_max)
                    self.amt_wool_send = amt
                    txt = self.__format_resource_text(amt, self.amt_wool_send_max)
                    self.txt_wool_send.set_text(txt)
                    self.__update_wool_exchange_text()

                # adjusting how much grain to send
                if self.btn_decr_grain_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_grain_send - 1, 0)
                    self.amt_grain_send = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_send_max)
                    self.txt_grain_send.set_text(txt)
                    self.__update_grain_exchange_text()

                if self.btn_incr_grain_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_grain_send + 1, self.amt_grain_send_max)
                    self.amt_grain_send = amt
                    txt = self.__format_resource_text(amt, self.amt_grain_send_max)
                    self.txt_grain_send.set_text(txt)
                    self.__update_grain_exchange_text()

                # adjusting how much brick to send
                if self.btn_decr_brick_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_brick_send - 1, 0)
                    self.amt_brick_send = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_send_max)
                    self.txt_brick_send.set_text(txt)
                    self.__update_brick_exchange_text()

                if self.btn_incr_brick_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_brick_send + 1, self.amt_brick_send_max)
                    self.amt_brick_send = amt
                    txt = self.__format_resource_text(amt, self.amt_brick_send_max)
                    self.txt_brick_send.set_text(txt)
                    self.__update_brick_exchange_text()

                # adjusting how much ore to send
                if self.btn_decr_ore_send.rect.collidepoint(mouse_pos):
                    amt = max(self.amt_ore_send - 1, 0)
                    self.amt_ore_send = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_send_max)
                    self.txt_ore_send.set_text(txt)
                    self.__update_ore_exchange_text()

                if self.btn_incr_ore_send.rect.collidepoint(mouse_pos):
                    amt = min(self.amt_ore_send + 1, self.amt_ore_send_max)
                    self.amt_ore_send = amt
                    txt = self.__format_resource_text(amt, self.amt_ore_send_max)
                    self.txt_ore_send.set_text(txt)
                    self.__update_ore_exchange_text()

                # choosing which resource to receive in exchange for lumber
                if self.btn_decr_res_1.rect.collidepoint(mouse_pos):
                    idx = self.lumber_returns.index(self.chosen_lumber_return)
                    idx = (idx - 1) % len(self.lumber_returns)
                    self.chosen_lumber_return = self.lumber_returns[idx]
                    self.__update_lumber_exchange_text()

                if self.btn_incr_res_1.rect.collidepoint(mouse_pos):
                    idx = self.lumber_returns.index(self.chosen_lumber_return)
                    idx = (idx + 1) % len(self.lumber_returns)
                    self.chosen_lumber_return = self.lumber_returns[idx]
                    self.__update_lumber_exchange_text()

                # choosing which resource to receive in exchange for wool
                if self.btn_decr_res_2.rect.collidepoint(mouse_pos):
                    idx = self.wool_returns.index(self.chosen_wool_return)
                    idx = (idx - 1) % len(self.wool_returns)
                    self.chosen_wool_return = self.wool_returns[idx]
                    self.__update_wool_exchange_text()

                if self.btn_incr_res_2.rect.collidepoint(mouse_pos):
                    idx = self.wool_returns.index(self.chosen_wool_return)
                    idx = (idx + 1) % len(self.wool_returns)
                    self.chosen_wool_return = self.wool_returns[idx]
                    self.__update_wool_exchange_text()

                # choosing which resource to receive in exchange for grain
                if self.btn_decr_res_3.rect.collidepoint(mouse_pos):
                    idx = self.grain_returns.index(self.chosen_grain_return)
                    idx = (idx - 1) % len(self.grain_returns)
                    self.chosen_grain_return = self.grain_returns[idx]
                    self.__update_grain_exchange_text()

                if self.btn_incr_res_3.rect.collidepoint(mouse_pos):
                    idx = self.grain_returns.index(self.chosen_grain_return)
                    idx = (idx + 1) % len(self.grain_returns)
                    self.chosen_grain_return = self.grain_returns[idx]
                    self.__update_grain_exchange_text()

                # choosing which resource to receive in exchange for brick
                if self.btn_decr_res_4.rect.collidepoint(mouse_pos):
                    idx = self.brick_returns.index(self.chosen_brick_return)
                    idx = (idx - 1) % len(self.brick_returns)
                    self.chosen_brick_return = self.brick_returns[idx]
                    self.__update_brick_exchange_text()

                if self.btn_incr_res_4.rect.collidepoint(mouse_pos):
                    idx = self.brick_returns.index(self.chosen_brick_return)
                    idx = (idx + 1) % len(self.brick_returns)
                    self.chosen_brick_return = self.brick_returns[idx]
                    self.__update_brick_exchange_text()

                # choosing which resource to receive in exchange for ore
                if self.btn_decr_res_5.rect.collidepoint(mouse_pos):
                    idx = self.ore_returns.index(self.chosen_ore_return)
                    idx = (idx - 1) % len(self.ore_returns)
                    self.chosen_ore_return = self.ore_returns[idx]
                    self.__update_ore_exchange_text()

                if self.btn_incr_res_5.rect.collidepoint(mouse_pos):
                    idx = self.ore_returns.index(self.chosen_ore_return)
                    idx = (idx + 1) % len(self.ore_returns)
                    self.chosen_ore_return = self.ore_returns[idx]
                    self.__update_ore_exchange_text()

                # clicking the 'make trade' button
                if self.btn_make_trade.rect.collidepoint(mouse_pos):
                    self.__make_trade()
                    self.app.set_view(self.app.game_view)


    def on_update(self):
        pass


    def __update_lumber_exchange_text(self):
        type_send = ResourceType.LUMBER
        amt_send = self.amt_lumber_send
        type_return = self.chosen_lumber_return
        amt_return = self.__calculate_exchange(type_send, amt_send, type_return)
        self.txt_res_1.set_text(f"{amt_return} {type_return.value}")


    def __update_wool_exchange_text(self):
        type_send = ResourceType.WOOL
        amt_send = self.amt_wool_send
        type_return = self.chosen_wool_return
        amt_return = self.__calculate_exchange(type_send, amt_send, type_return)
        self.txt_res_2.set_text(f"{amt_return} {type_return.value}")


    def __update_grain_exchange_text(self):
        type_send = ResourceType.GRAIN
        amt_send = self.amt_grain_send
        type_return = self.chosen_grain_return
        amt_return = self.__calculate_exchange(type_send, amt_send, type_return)
        self.txt_res_3.set_text(f"{amt_return} {type_return.value}")


    def __update_brick_exchange_text(self):
        type_send = ResourceType.BRICK
        amt_send = self.amt_brick_send
        type_return = self.chosen_brick_return
        amt_return = self.__calculate_exchange(type_send, amt_send, type_return)
        self.txt_res_4.set_text(f"{amt_return} {type_return.value}")


    def __update_ore_exchange_text(self):
        type_send = ResourceType.ORE
        amt_send = self.amt_ore_send
        type_return = self.chosen_ore_return
        amt_return = self.__calculate_exchange(type_send, amt_send, type_return)
        self.txt_res_5.set_text(f"{amt_return} {type_return.value}")


    def __find_best_harbour_rate(self, player, resource_type):
        harbours = self.app.game_controller.get_harbours()
        ratio = 4

        for harbour in harbours:
            # check if player has access to any-type harbour
            if harbour.get_type() == ResourceType.ANY:
                for settlement in harbour.get_settlements():
                    if settlement.owner == player:
                        # set the exchange ratio to 3:1, unless a better
                        # ratio is already being used at a different
                        # harbour
                        if ratio > 3:
                            ratio = 3

            # check if the player has access to the harbour of the
            # resource type they are sending
            if harbour.get_type() == resource_type:
                for settlement in harbour.get_settlements():
                    if settlement.owner == player:
                        # if so, the exchange ratio is 2:1
                        ratio = 2

        return ratio


    def __calculate_exchange(self, type1, amount1, type2):
        ratio = self.__find_best_harbour_rate(self.trade_sender, type1)
        amount2 = amount1 // ratio
        maximum_exchange = 0

        if type2 == ResourceType.LUMBER:
            maximum_exchange = self.bank.count_lumber()

        elif type2 == ResourceType.WOOL:
            maximum_exchange = self.bank.count_wool()

        elif type2 == ResourceType.GRAIN:
            maximum_exchange = self.bank.count_grain()

        elif type2 == ResourceType.BRICK:
            maximum_exchange = self.bank.count_brick()

        elif type2 == ResourceType.ORE:
            maximum_exchange = self.bank.count_ore()

        amount2 = min(amount2, maximum_exchange)

        return amount2


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
    

    def __make_trade(self):
        self.amt_lumber_receive = 0


        # send resources from the trade initiator to the receiver
        self.trade_sender.add_resources(lumber = self.amt_lumber_receive,
                                        wool = self.amt_wool_receive,
                                        grain = self.amt_grain_receive,
                                        brick = self.amt_brick_receive,
                                        ore = self.amt_ore_receive)
        
        self.bank.remove_resources(lumber = self.amt_lumber_receive,
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
        
        self.bank.add_resources(lumber = self.amt_lumber_send,
                                wool = self.amt_wool_send,
                                grain = self.amt_grain_send,
                                brick = self.amt_brick_send,
                                ore = self.amt_ore_send)