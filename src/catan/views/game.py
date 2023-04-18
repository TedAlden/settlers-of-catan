import time
import pygame

from math import sqrt

from catan.models.game import GameModel
from catan.models.settlement import Settlement
from catan.models.city import City

from catan.views.components.bankpanel import BankPanel
from catan.views.components.inventorypanel import InventoryPanel
from catan.views.components.playerpanel import PlayerPanel
from catan.views.components.button import Button
from catan.views.components.dice import DiceView

from catan.type import ActionType, TerrainType
from catan.util.shapes import draw_city, draw_hextile, draw_road, draw_settlement, draw_robber

pygame.font.init()
FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)
BACKGROUND_IMAGE = pygame.image.load("src\\catan\\assets\\images\\background.png")
SETTLEMENT_COLOURS = {
    TerrainType.FIELD : "#e6d85e",
    TerrainType.PASTURE : "#5fc73a",
    TerrainType.FOREST : "#168a35",
    TerrainType.HILL : "#e09e2b",
    TerrainType.MOUNTAIN : "#8c8c8c",
    TerrainType.DESERT : "#b5ac6e"
}


class GameView:

    def __init__(self, controller):
        self.controller = controller  # game controller

        self.selected = []
        self.last_tick = 0

        self.hex_radius = 60
        self.hex_height = self.hex_radius * sqrt(3)

        # dice
        dice1, dice2 = self.controller.get_dice()
        self.dice1 = DiceView(dice1, (74, 740))
        self.dice2 = DiceView(dice2, (166, 740))

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

        # UI panels
        players = self.controller.get_players()
        self.bank_table = BankPanel(self.controller.get_bank(), (970, 10))
        self.inventory_table = InventoryPanel((320, 680))
        self.player_table_1 = PlayerPanel(players[0], (970, 168))
        self.player_table_2 = PlayerPanel(players[1], (970, 326))
        self.player_table_3 = PlayerPanel(players[2], (970, 484))
        self.player_table_4 = PlayerPanel(players[3], (970, 642))

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
                    pass
                    # TODO

                if self.btn_save.rect.collidepoint(mouse_pos):
                    # TODO: include date and time in save file name?
                    name = "game1.json"
                    GameModel.save_to_file(self.controller.model, name)

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
                    # TODO

                if self.btn_roll_dice.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.roll_dice()

                if self.btn_player_trade.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    # TODO

                if self.btn_bank_trade.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    # TODO

                if self.btn_next_turn.rect.collidepoint(mouse_pos):
                    self.on_finish_action()
                    self.controller.next_turn()

                # clicking on settlement
                for settlement in self.controller.get_settlements():
                    if settlement.rect.collidepoint(mouse_pos):
                        if self.controller.action == ActionType.PLACE_ROAD:
                            self.on_place_road(settlement)

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


    def on_place_road(self, settlement):
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

        # update resource panels on right hand side of screen UI
        self.bank_table.update()
        self.inventory_table.set_player(self.controller.get_current_player())
        self.inventory_table.update()
        self.player_table_1.update()
        self.player_table_2.update()
        self.player_table_3.update()
        self.player_table_4.update()


    def on_render(self, screen):
        # draw catan background
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # draw the boards roads
        for road in self.controller.get_roads():
            pos1, pos2 = road.settlements[0].get_pos(), road.settlements[1].get_pos()
            draw_road(screen, pos1, pos2, road.owner.colour)

        # draw the boards hex tiles
        for tile in self.controller.get_tiles():
            col = SETTLEMENT_COLOURS[tile.type]
            draw_hextile(screen, col, self.hex_radius - 5, tile.get_pos(), tile.number)

            # draw robber if it is placed here
            robber = self.controller.get_robber()
            if tile == robber.get_hex():
                x, y = tile.get_pos()
                draw_robber(screen, (x, y + 30), robber.get_owner().colour)

        # draw the boards settlements
        for settlement in self.controller.get_settlements():
            # draw settlement
            if isinstance(settlement, Settlement):
                colour = "#ffffff" if settlement.selected else settlement.owner.colour
                draw_settlement(screen, colour, settlement.get_pos())

            # draw city
            elif isinstance(settlement, City):
                colour = "#ffffff" if settlement.selected else settlement.owner.colour
                draw_city(screen, colour, settlement.get_pos())

            # draw empty settlement marker when placing board pieces
            elif self.controller.action in (ActionType.PLACE_CITY,
                                            ActionType.PLACE_ROAD,
                                            ActionType.PLACE_SETTLEMENT):
                colour = "#ffffff" if settlement.selected else "#cccccc"
                pygame.draw.circle(screen, colour, settlement.get_pos(), 10)

        # draw dice
        self.dice1.draw(screen)
        self.dice2.draw(screen)

        # draw UI panels
        self.bank_table.draw(screen)
        self.inventory_table.draw(screen)
        self.player_table_1.draw(screen)
        self.player_table_2.draw(screen)
        self.player_table_3.draw(screen)
        self.player_table_4.draw(screen)

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

        # display current player
        p = self.controller.get_current_player().name
        screen.blit(FONT.render(f"Turn: {p}", True, "white"), (260, 30))

        # display game time
        t = self.get_time()
        screen.blit(FONT.render(f"Time: {t}", True, "white"), (260, 60))

        # display current action
        a = self.controller.action.value
        screen.blit(FONT.render(f"Currently: {a}", True, "white"), (260, 90))
