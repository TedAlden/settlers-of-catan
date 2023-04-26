import time
import pygame

from math import sqrt

from catan.models.game import GameModel
from catan.models.settlement import Settlement
from catan.models.city import City
from catan.views.bank_trade import BankTradeView
from catan.views.components.button import Button
from catan.type import ActionType, TerrainType
from catan.util.pathresolver import resolve_path
from catan.util.shapes import draw_city, draw_road, draw_settlement, draw_robber
from catan.views.playertrade import PlayerTradeView

pygame.font.init()

TERRAIN_NUMBER_FONT = pygame.font.SysFont(None, 32)
FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)

BACKGROUND_IMAGE = pygame.image.load(resolve_path("catan/assets/images/background.png"))

RC_LUMBER_SMALL = pygame.image.load(resolve_path("catan/assets/images/res_card_lumber_small.png"))
RC_WOOL_SMALL = pygame.image.load(resolve_path("catan/assets/images/res_card_wool_small.png"))
RC_GRAIN_SMALL = pygame.image.load(resolve_path("catan/assets/images/res_card_grain_small.png"))
RC_BRICK_SMALL = pygame.image.load(resolve_path("catan/assets/images/res_card_brick_small.png"))
RC_ORE_SMALL = pygame.image.load(resolve_path("catan/assets/images/res_card_ore_small.png"))

RC_LUMBER = pygame.image.load(resolve_path("catan/assets/images/res_card_lumber.png"))
RC_WOOL = pygame.image.load(resolve_path("catan/assets/images/res_card_wool.png"))
RC_GRAIN = pygame.image.load(resolve_path("catan/assets/images/res_card_grain.png"))
RC_BRICK = pygame.image.load(resolve_path("catan/assets/images/res_card_brick.png"))
RC_ORE = pygame.image.load(resolve_path("catan/assets/images/res_card_ore.png"))

DC_KNIGHT = pygame.image.load(resolve_path("catan/assets/images/dev_card_knight.png"))
DC_ROAD = pygame.image.load(resolve_path("catan/assets/images/dev_card_road.png"))
DC_PLENTY = pygame.image.load(resolve_path("catan/assets/images/dev_card_plenty.png"))
DC_MONOPOLY = pygame.image.load(resolve_path("catan/assets/images/dev_card_monopoly.png"))
DC_VP = pygame.image.load(resolve_path("catan/assets/images/dev_card_knight.png"))

DEV_CARD = pygame.image.load(resolve_path("catan/assets/images/dev_card_back.png"))
RES_CARD = pygame.image.load(resolve_path("catan/assets/images/res_card_back.png"))
VP_ICON = pygame.image.load(resolve_path("catan/assets/images/vp_icon.png"))
LARGEST_ARMY = pygame.image.load(resolve_path("catan/assets/images/largest_army.png"))
LONGEST_ROAD = pygame.image.load(resolve_path("catan/assets/images/longest_road.png"))

HEXTILE_IMAGES = {
    TerrainType.FIELD : pygame.image.load(resolve_path("catan/assets/images/hex_grain.png")),
    TerrainType.PASTURE : pygame.image.load(resolve_path("catan/assets/images/hex_wool.png")),
    TerrainType.FOREST : pygame.image.load(resolve_path("catan/assets/images/hex_lumber.png")),
    TerrainType.HILL : pygame.image.load(resolve_path("catan/assets/images/hex_brick.png")),
    TerrainType.MOUNTAIN : pygame.image.load(resolve_path("catan/assets/images/hex_ore.png")),
    TerrainType.DESERT : pygame.image.load(resolve_path("catan/assets/images/hex_desert.png")),
}

DICE_IMAGES = {
    1: pygame.image.load(resolve_path("catan/assets/images/dice_1.png")),
    2: pygame.image.load(resolve_path("catan/assets/images/dice_2.png")),
    3: pygame.image.load(resolve_path("catan/assets/images/dice_3.png")),
    4: pygame.image.load(resolve_path("catan/assets/images/dice_4.png")),
    5: pygame.image.load(resolve_path("catan/assets/images/dice_5.png")),
    6: pygame.image.load(resolve_path("catan/assets/images/dice_6.png"))
}


class GameView:

    def __init__(self, controller, app):
        self.controller = controller  # game controller
        self.app = app

        self.selected = []
        self.last_tick = 0

        self.hex_radius = 60
        self.hex_height = self.hex_radius * sqrt(3)

        # UI buttons (left hand side)
        self.btn_menu = Button("Menu", (10, 10))
        self.btn_save = Button("Save", (10, 70))

        self.btn_settlement = Button("Build Settlement", (10, 170))
        self.btn_road = Button("Build Road", (10, 230))
        self.btn_city = Button("Upgrade to City", (10, 290))
        self.btn_dev_card = Button("Development Card", (10, 350))

        self.btn_roll_dice = Button("Roll Dice", (10, 450))
        self.btn_player_trade = Button("Player Trade", (10, 510))
        self.btn_bank_trade = Button("Bank Trade", (10, 570))
        self.btn_next_turn = Button("End Turn", (10, 630))

        # calculate coordinates of terrain tiles and settlements
        relative_coords = [
            (self.hex_radius / 2, self.hex_height / 2),
            (self.hex_radius, 0),
            (self.hex_radius / 2, -(self.hex_height / 2)),
            (-(self.hex_radius / 2), -(self.hex_height / 2)),
            (-self.hex_radius, 0),
            (-(self.hex_radius / 2), self.hex_height / 2)
        ]

        visited_settlements = []
        for terrain_tile in self.controller.get_tiles():
            # convert axial terrain coords to screen/pixel coords.
            tx, ty = terrain_tile.axial_coord
            x = tx * 3/2 * self.hex_radius
            y = tx * 0.5 * self.hex_height + ty * self.hex_height
            terrain_tile.set_pos(x + 640, y + 400)  # shift grid
            # calculate screen coords for each settlement based on the
            # terrain that it neighbours.
            for settlement in self.controller.model.board.get_surrounding_nodes(terrain_tile):
                if settlement not in visited_settlements:
                    idx = self.controller.model.board._graph[terrain_tile].index(settlement)
                    x = terrain_tile.get_pos()[0] + relative_coords[idx][0]
                    y = terrain_tile.get_pos()[1] - relative_coords[idx][1]
                    settlement.set_pos(x, y)
                    visited_settlements.append(settlement)


    def on_finish_action(self):
        for settlement in self.selected:
            settlement.selected = False

        self.selected.clear()
        self.controller.action = ActionType.NONE


    def get_time(self):
        seconds = self.controller.model.game_time / 1000
        return time.strftime('%H:%M:%S', time.gmtime(seconds))


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # clicking on left hand side UI buttons...
                if self.btn_menu.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.menu_view)

                if self.btn_save.rect.collidepoint(mouse_pos):
                    path = resolve_path("saves/game1.json")
                    GameModel.save_to_file(self.controller.model, path)

                if self.btn_settlement.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.action = ActionType.PLACE_SETTLEMENT

                if self.btn_road.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.action = ActionType.PLACE_ROAD

                if self.btn_city.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.action = ActionType.PLACE_CITY

                if self.btn_dev_card.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.__handle_buy_development_card()

                if self.btn_roll_dice.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.roll_dice()

                if self.btn_player_trade.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.app.player_trade_view = PlayerTradeView(self.app)
                    self.app.set_view(self.app.player_trade_view)

                if self.btn_bank_trade.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.app.bank_trade_view = BankTradeView(self.app)
                    self.app.set_view(self.app.bank_trade_view)

                if self.btn_next_turn.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.next_turn()

                # clicking on settlement
                for settlement in self.controller.get_settlements():
                    if settlement.rect.collidepoint(mouse_pos):
                        if self.controller.action == ActionType.PLACE_ROAD:
                            self.__handle_place_road(settlement)

                        elif self.controller.action == ActionType.PLACE_SETTLEMENT:
                            self.controller.place_settlement(settlement)
                            self.on_finish_action()

                        elif self.controller.action == ActionType.PLACE_CITY:
                            self.controller.place_city(settlement)
                            self.on_finish_action()

                # clicking on terrain tile
                for terrain in self.controller.get_tiles():
                    if terrain.rect.collidepoint(mouse_pos):
                        if self.controller.action == ActionType.PLACE_ROBBER:
                            self.controller.place_robber(terrain)
                            self.on_finish_action()

    
    def __handle_buy_development_card(self):
        
        # TODO

        pass


    def __handle_place_road(self, settlement):
        # select first settlement
        if len(self.selected) == 0:
            self.selected.append(settlement)
            settlement.selected = True

        # deselect the first settlement if clicked again
        elif settlement == self.selected[0]:
            self.on_finish_action()

        # select second settlement
        elif len(self.selected) == 1:
            self.selected.append(settlement)
            self.controller.place_road(*self.selected)
            self.on_finish_action()


    def on_update(self):
        # update game time
        tick = pygame.time.get_ticks()
        delta_time = tick - self.last_tick
        self.last_tick = tick
        self.controller.model.game_time += delta_time


    def on_render(self, screen):
        # draw catan background
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # draw board
        self.__draw_board(screen)

        # draw UI panels
        bank = self.controller.get_bank()
        current_player = self.controller.get_current_player()
        players = self.controller.get_players()
        
        self.__draw_bank_panel(screen, bank, (970, 10))
        self.__draw_inventory_panel(screen, current_player, (320, 680))
        self.__draw_player_panel(screen, players[0], (970, 168))
        self.__draw_player_panel(screen, players[1], (970, 326))
        self.__draw_player_panel(screen, players[2], (970, 484))
        self.__draw_player_panel(screen, players[3], (970, 642))

        # draw dice
        self.__draw_dice(screen)

        # draw UI buttons
        self.btn_menu.draw(screen)
        self.btn_save.draw(screen)

        self.btn_settlement.draw(screen)
        self.btn_road.draw(screen)
        self.btn_city.draw(screen)
        self.btn_dev_card.draw(screen)

        self.btn_roll_dice.draw(screen)
        self.btn_player_trade.draw(screen)
        self.btn_bank_trade.draw(screen)
        self.btn_next_turn.draw(screen)

        # display current player, game time, current action
        p = self.controller.get_current_player().name
        t = self.get_time()
        a = self.controller.action.value
        screen.blit(FONT.render(f"Turn: {p}", True, "white"), (260, 30))
        screen.blit(FONT.render(f"Time: {t}", True, "white"), (260, 60))      
        screen.blit(FONT.render(f"Currently: {a}", True, "white"), (260, 90))

    
    def __draw_board(self, screen):
        # draw the boards roads
        for road in self.controller.get_roads():
            pos1, pos2 = road.settlements[0].get_pos(), road.settlements[1].get_pos()
            draw_road(screen, pos1, pos2, road.owner.colour)

        # draw the boards hex tiles
        for tile in self.controller.get_tiles():
            # draw terrain hex
            x, y = tile.get_pos()
            img = HEXTILE_IMAGES[tile.type]
            half_w, half_h = img.get_width() / 2, img.get_height() / 2
            screen.blit(img, (x - half_w, y - half_h))

            # draw hex tile number
            if tile.number > 0:
                img = TERRAIN_NUMBER_FONT.render(str(tile.number), True, "white")
                w, h = img.get_rect().width, img.get_rect().height
                screen.blit(img, (x - 0.5 * w, y - 0.5 * h))

            # draw robber if it is placed here
            robber = self.controller.get_robber()
            if tile == robber.get_hex():
                draw_robber(screen, (x, y + 30), robber.get_owner().colour)

        # draw the boards settlements
        for settlement in self.controller.get_settlements():
            x, y = settlement.get_pos()
            # draw settlement
            if isinstance(settlement, Settlement):
                colour = "#ffffff" if settlement.selected else settlement.owner.colour
                draw_settlement(screen, colour, (x, y))

            # draw city
            elif isinstance(settlement, City):
                colour = "#ffffff" if settlement.selected else settlement.owner.colour
                draw_city(screen, colour, (x, y))

            # draw empty settlement indicator when placing board pieces
            elif self.controller.action in (ActionType.PLACE_CITY,
                                            ActionType.PLACE_ROAD,
                                            ActionType.PLACE_SETTLEMENT):
                colour = "#ffffff" if settlement.selected else "#cccccc"
                pygame.draw.circle(screen, colour, (x, y), 10)


    def __draw_dice(self, screen):
        dice1, dice2 = self.controller.get_dice()

        image1 = DICE_IMAGES[dice1.value]
        image2 = DICE_IMAGES[dice2.value]

        screen.blit(image1, (42, 708))        
        screen.blit(image2, (134, 708))


    def __draw_bank_panel(self, screen, bank, pos):
        x, y, w, h = *pos, 300, 148

        lumber = bank.count_lumber()
        wool = bank.count_wool()
        grain = bank.count_grain()
        brick = bank.count_brick()
        ore = bank.count_ore()
        devs = bank.count_development_cards()

        pygame.draw.rect(screen, "#999999", (x, y, w, h))

        screen.blit(FONT.render("Bank", True, "white"), (x+10, y+10))

        screen.blit(RC_LUMBER_SMALL, (x+10, y+40))
        screen.blit(RC_WOOL_SMALL, (x+58, y+40))
        screen.blit(RC_GRAIN_SMALL, (x+106, y+40))
        screen.blit(RC_BRICK_SMALL, (x+154, y+40))
        screen.blit(RC_ORE_SMALL, (x+202, y+40))
        screen.blit(DEV_CARD, (x+250, y+40))

        screen.blit(FONT.render(str(lumber), True, "white"), (x+20, y+108))
        screen.blit(FONT.render(str(wool), True, "white"), (x+68, y+108))
        screen.blit(FONT.render(str(grain), True, "white"), (x+116, y+108))
        screen.blit(FONT.render(str(brick), True, "white"), (x+164, y+108))
        screen.blit(FONT.render(str(ore), True, "white"), (x+212, y+108))
        screen.blit(FONT.render(str(devs), True, "white"), (x+260, y+108))

    
    def __draw_player_panel(self, screen, player, pos):
        x, y, w, h = *pos, 300, 148

        name = player.name
        colour = player.colour
        vp = player.count_vp()
        road = player.count_longest_road()
        army = player.count_army()
        res = player.count_resource_cards()
        dev = player.count_development_cards()

        pygame.draw.rect(screen, "#999999", (x, y, w, h))

        pygame.draw.circle(screen, colour, (x+19, y+19), 9)
        screen.blit(FONT.render(name, True, colour), (x+38, y+10))

        screen.blit(RES_CARD, (x+10, y+40))
        screen.blit(DEV_CARD, (x+58, y+40))
        screen.blit(VP_ICON, (x+106, y+40))

        # FIXME: only show if player has longest road...
        screen.blit(LONGEST_ROAD, (x+160, y+24))

        # FIXME: only show if player has largest army...
        screen.blit(LARGEST_ARMY, (x+230, y+24))

        screen.blit(FONT.render(str(res), True, "white"), (x+24, y+108))
        screen.blit(FONT.render(str(dev), True, "white"), (x+72, y+108))
        screen.blit(FONT.render(str(vp), True, "white"), (x+120, y+108))

    
    def __draw_inventory_panel(self, screen, player, pos):
        x, y, w, h = *pos, 640, 120

        lumber = player.count_lumber()
        wool = player.count_wool()
        grain = player.count_grain()
        brick = player.count_brick()
        ore = player.count_ore()
        knight = player.count_card_knight()
        road = player.count_card_road()
        plenty = player.count_card_year_plenty()
        monopoly = player.count_card_monopoly()
        vp = player.count_card_vp()

        pygame.draw.rect(screen, "#999999", (x, y, w, h))

        screen.blit(RC_LUMBER, (x+10, y+10))
        screen.blit(RC_WOOL, (x+68, y+10))
        screen.blit(RC_GRAIN, (x+126, y+10))
        screen.blit(RC_BRICK, (x+184, y+10))
        screen.blit(RC_ORE, (x+242, y+10))

        screen.blit(FONT.render(str(lumber), True, "white"), (x+28, y+90))
        screen.blit(FONT.render(str(wool), True, "white"), (x+86, y+90))
        screen.blit(FONT.render(str(grain), True, "white"), (x+144, y+90))
        screen.blit(FONT.render(str(brick), True, "white"), (x+202, y+90))
        screen.blit(FONT.render(str(ore), True, "white"), (x+260, y+90))

        screen.blit(DC_KNIGHT, (x+350, y+10))
        screen.blit(DC_ROAD, (x+408, y+10))
        screen.blit(DC_PLENTY, (x+466, y+10))
        screen.blit(DC_MONOPOLY, (x+524, y+10))
        screen.blit(DC_VP, (x+582, y+10))

        screen.blit(FONT.render(str(knight), True, "white"), (x+368, y+90))
        screen.blit(FONT.render(str(road), True, "white"), (x+426, y+90))
        screen.blit(FONT.render(str(plenty), True, "white"), (x+484, y+90))
        screen.blit(FONT.render(str(monopoly), True, "white"), (x+542, y+90))
        screen.blit(FONT.render(str(vp), True, "white"), (x+600, y+90))
