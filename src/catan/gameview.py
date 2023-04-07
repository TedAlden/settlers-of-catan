import pygame
import time

from catan.board import Board
from catan.type import ActionType, TerrainType
from catan.player import Player
from catan.pieces import EmptySettlement, Settlement, City
from catan.ui import Button, Dice, PlayerPanel, BankPanel
from catan.bank import Bank


pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont(None, 32)
EIGHT_BIT_FONT = pygame.font.Font("src\\catan\\assets\\fonts\\EightBitDragon-anqx.ttf", 18)
BACKGROUND_IMAGE = pygame.image.load("src\\catan\\assets\\images\\background.png")


class GameView:

    def __init__(self):
        # Testing board saving/loading always works
        new_random_board = Board.make_random()
        Board.save_to_file(new_random_board, "board.json")

        # Game objects
        self.board = Board.load_from_file("board.json")
        self.bank = Bank()
        self.players = [
            Player("Player 1", "red"),
            Player("Player 2", "green"),
            Player("Player 3", "blue"),
            Player("Player 4", "purple")
        ]

        # Gameplay variables
        self.selected = []  # stores the settlements selected on the UI
        self.action = ActionType.NONE  # current player action
        self.current_player = self.players[0]

        # Dice
        self.dice1 = Dice((74, 610))
        self.dice2 = Dice((166, 610))

        # Action buttons
        self.btn_menu = Button("Menu", (10, 10), EIGHT_BIT_FONT)

        self.btn_place_settlement = Button("Settlement", (10, 110), EIGHT_BIT_FONT)
        self.btn_place_road = Button("Road", (10, 170), EIGHT_BIT_FONT)
        self.btn_place_city = Button("City", (10, 230), EIGHT_BIT_FONT)
        self.btn_buy_dev_card = Button("Development card", (10, 290), EIGHT_BIT_FONT)

        self.btn_roll_dice = Button("Roll dice", (10, 390), EIGHT_BIT_FONT)
        self.btn_start_trade = Button("Trade", (10, 450), EIGHT_BIT_FONT)
        self.btn_next_turn = Button("End turn", (10, 510), EIGHT_BIT_FONT)

        # UI textboxes
        self.bank_table = BankPanel(self.bank, (970, 10))
        self.player_table_1 = PlayerPanel(self.players[0], (970, 240))
        self.player_table_2 = PlayerPanel(self.players[1], (970, 380))
        self.player_table_3 = PlayerPanel(self.players[2], (970, 520))
        self.player_table_4 = PlayerPanel(self.players[3], (970, 660))
        

    def on_update(self):
        self.player_table_1.update()
        self.player_table_2.update()
        self.player_table_3.update()
        self.player_table_4.update()


    def on_render(self, screen):
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Draw board terrain tiles, roads, settlements/cities
        for road in self.board.roads:
            road.draw(screen)

        for terrain_tile in self.board.terrain_tiles.values():
            terrain_tile.draw(screen)

        for settlement in self.board.settlements:
            if isinstance(settlement, (Settlement, City)):
                settlement.draw(screen)

            elif self.action in (ActionType.PLACE_CITY,
                                 ActionType.PLACE_ROAD,
                                 ActionType.PLACE_SETTLEMENT):
                settlement.draw(screen)

        # Draw bank/player tables to show resource statistics
        self.bank_table.draw(screen)
        self.player_table_1.draw(screen)
        self.player_table_2.draw(screen)
        self.player_table_3.draw(screen)
        self.player_table_4.draw(screen)

        # Draw dice
        self.dice1.draw(screen)
        self.dice2.draw(screen)

        # Draw controls buttons
        self.btn_menu.draw(screen)
        self.btn_place_settlement.draw(screen)
        self.btn_place_road.draw(screen)
        self.btn_place_city.draw(screen)
        self.btn_buy_dev_card.draw(screen)
        self.btn_roll_dice.draw(screen)
        self.btn_start_trade.draw(screen)
        self.btn_next_turn.draw(screen)

        # Draw textboxes in bottom left corner
        current_player = self.current_player.name
        game_timer = time.strftime('%H:%M:%S', time.gmtime(int(pygame.time.get_ticks()/1000)))
        screen.blit(EIGHT_BIT_FONT.render(f"Player: {current_player}", True, "white"), (10, 700))
        screen.blit(EIGHT_BIT_FONT.render(f"Action: {self.action}", True, "white"), (10, 730))
        screen.blit(EIGHT_BIT_FONT.render(f"Time: {game_timer}", True, "white"), (10, 760))


    def finish_action(self):
        # When finishing an action, deselect any settlement markers that
        # were selected, and set the action back to none. This will
        # happen whether an action completes successfully or not.
        for settlement in self.selected:
            settlement.selected = False
        self.selected.clear()
        self.action = ActionType.NONE


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_pos = pygame.mouse.get_pos()
                
                if self.btn_next_turn.rect.collidepoint(mouse_pos):
                    self.finish_action()
                    self._on_next_turn()

                if self.btn_place_settlement.rect.collidepoint(mouse_pos):
                    self.finish_action()
                    self.action = ActionType.PLACE_SETTLEMENT

                if self.btn_place_road.rect.collidepoint(mouse_pos):
                    self.finish_action()
                    self.action = ActionType.PLACE_ROAD

                if self.btn_place_city.rect.collidepoint(mouse_pos):
                    self.finish_action()
                    self.action = ActionType.PLACE_CITY

                if self.btn_roll_dice.rect.collidepoint(mouse_pos):
                    self._on_dice_roll()

                for settlement in self.board.settlements:
                    if settlement.rect.collidepoint(mouse_pos):
                        if self.action == ActionType.PLACE_ROAD:
                            self._on_place_road(settlement)
                        elif self.action == ActionType.PLACE_SETTLEMENT:
                            self._on_place_settlement(settlement)
                        elif self.action == ActionType.PLACE_CITY:
                            self._on_place_city(settlement)

                for terrain in self.board.terrain_tiles.values():
                    if terrain.rect.collidepoint(mouse_pos):
                        if self.action == ActionType.PLACE_ROBBER:
                            self._on_place_robber(terrain)


    def _on_place_road(self, settlement):
        # select first settlement
        if len(self.selected) == 0:
            self.selected.append(settlement)
            settlement.selected = True

        # select second settlement.
        elif len(self.selected) == 1:
            # FIXME: stop players from placing roads over other players
            # settlements??

            # check node not already selected, and that the node is
            # close enough to the other selected node
            if settlement not in self.selected and settlement in self.board.get_surrounding_nodes(self.selected[0]):
                self.selected.append(settlement)
                # check if the road attempting to be placed touches one
                # of the players existing roads
                touching_own_road = False
                for node in self.selected:
                    for road in self.board.roads:
                        if road.owner == self.current_player and node in road.settlements:
                            touching_own_road = True

                # check if the road attempting to be placed touches
                # one of the players existing settlements
                touching_own_settlement = False
                if self.selected[0].owner == self.current_player or self.selected[1].owner == self.current_player:
                    touching_own_settlement = True
                # place the road if it doesn't already exist, and is
                # connected to players existing roads/settlements
                road_occupied = self.board.has_road(*self.selected)
                # finally place road if all conditions are valid
                if (not road_occupied) and (touching_own_road or touching_own_settlement):
                    self.board.add_road(*self.selected, self.current_player)
                    self.current_player.roads += 1
                # deselect settlements when road successfully placed
                self.finish_action()

            # deselect the first settlement if clicked again
            elif settlement == self.selected[0]:
                self.finish_action()


    def _on_place_settlement(self, settlement):
        space_around = True  # no adjacent settlements
        touching_roads = False  # touching players own roads
        for node in self.board.get_surrounding_nodes(settlement):
            # check that there is enough space around the node to  place
            # the settlement, i.e. no other settlements
            if isinstance(node, Settlement) or isinstance(node, City):
                space_around = False

            # check the settlement is touching one of the players
            # roads existing roads
            for road in self.board.roads:
                if settlement in road.settlements and node in road.settlements:
                    touching_roads = True

        # check if this is one of the players initial 2 settlements
        # being placed as this overrides the rule of it having to touch
        # a currently owned road
        placed_initial = self.current_player.count_settlements() >= 2
        # check if settlement is already owned by any player
        already_owned = not isinstance(settlement, EmptySettlement)
        # finally place settlement if all conditions are valid
        if not already_owned and space_around and (not placed_initial or touching_roads):
            self.board.add_settlement(settlement, self.current_player)
            self.current_player.settlements += 1

        self.finish_action()
    

    def _on_place_city(self, settlement):
        if settlement.owner == self.current_player:
            self.board.add_city(settlement)
            self.current_player.cities += 1
        self.finish_action()


    def _on_place_robber(self, terrain):
        pass


    def _on_dice_roll(self):
        self.dice1.roll()
        self.dice2.roll()
        total = self.dice1.value + self.dice2.value

        turn_info = f"\nRolled a {total}\n"
        
        for terrain_tile in self.board.terrain_tiles.values():
            if terrain_tile.number == total:
                for settlement in self.board.get_surrounding_nodes(terrain_tile):
                    if isinstance(settlement, (Settlement, City)):
                        collector = settlement.owner
                        # TODO: change collector if their is a robber
                        # if terrain_tile.robber != None:
                        #   collector = terrain_tile.robber.owner
                        amount = 2 if isinstance(settlement, City) else 1
                        name = collector.name

                        if terrain_tile.type == TerrainType.FOREST:
                            if self.bank.has_resources(lumber=1):
                                collector.add_resources(lumber=1)
                                self.bank.remove_resources(lumber=1)
                                turn_info += f"Given '{name}' {amount}x lumber\n"

                        elif terrain_tile.type == TerrainType.PASTURE:
                            if self.bank.has_resources(wool=1):
                                collector.add_resources(wool=1)
                                self.bank.remove_resources(wool=1)
                                turn_info += f"Given '{name}' {amount}x wool\n"

                        elif terrain_tile.type == TerrainType.FIELD:
                            if self.bank.has_resources(grain=1):
                                collector.add_resources(grain=1)
                                self.bank.remove_resources(grain=1)
                                turn_info += f"Given '{name}' {amount}x grain\n"

                        elif terrain_tile.type == TerrainType.HILL:
                            if self.bank.has_resources(brick=1):
                                collector.add_resources(brick=1)
                                self.bank.remove_resources(brick=1)
                                turn_info += f"Given '{name}' {amount}x brick\n"

                        elif terrain_tile.type == TerrainType.MOUNTAIN:
                            if self.bank.has_resources(ore=1):
                                collector.add_resources(ore=1)
                                self.bank.remove_resources(ore=1)
                                turn_info += f"Given '{name}' {amount}x ore\n"

        print(turn_info)


    def _on_next_turn(self):
        idx = self.players.index(self.current_player)
        idx = (idx + 1) % len(self.players)
        self.current_player = self.players[idx]
