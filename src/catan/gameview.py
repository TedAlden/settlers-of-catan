import pygame
from .board import Board
from .type import ActionType
from .player import Player
from .pieces import EmptySettlement, Settlement, City, Dice
from .ui import Button, TextBox


pygame.font.init()
BUTTON_FONT = pygame.font.SysFont(None, 32)


class GameView:

    def __init__(self):
        # testing board saving/loading always works
        b = Board.make_random()
        Board.save_to_file(b, "board.json")
        self.board = Board.load_from_file("board.json")
        self.players = [
            Player("Player 1", "red"),
            Player("Player 2", "blue"),
            Player("Player 3", "orange"),
            Player("Player 4", "white")
        ]

        self.selected = []  # stores the settlements selected on the UI
        self.action = ActionType.PLACE_SETTLEMENT
        self.current_player = self.players[0]

        # UI buttons
        self.dice1 = Dice(800, 684)
        self.dice2 = Dice(800, 764)
        self.btn_next_turn = Button("Next turn", 10, 10)
        self.btn_place_settlement = Button("Place settlement", 10, 42)
        self.btn_place_road = Button("Place road", 10, 74)
        self.btn_place_city = Button("Place city", 10, 106)

        # UI textboxes
        self.txt_current_player = TextBox(lambda: f"Current player: {self.current_player.name}", 10, 138)
        self.txt_current_action = TextBox(lambda: f"Current action: {self.action.name}", 10, 170)
        

    def deselect_settlements(self):
        # placing roads and settlements on the board requires selecting
        # settlements. events such as changing player, or changing
        # action should deselect any that are selected to avoid errors.
        for settlement in self.selected:
            settlement.selected = False
        self.selected.clear()


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_pos = pygame.mouse.get_pos()
                
                if self.btn_next_turn.rect.collidepoint(mouse_pos):
                    self.deselect_settlements()
                    idx = self.players.index(self.current_player)
                    idx = (idx + 1) % len(self.players)
                    self.current_player = self.players[idx]

                if self.btn_place_settlement.rect.collidepoint(mouse_pos):
                    self.deselect_settlements()
                    self.action = ActionType.PLACE_SETTLEMENT

                if self.btn_place_road.rect.collidepoint(mouse_pos):
                    self.deselect_settlements()
                    self.action = ActionType.PLACE_ROAD

                if self.btn_place_city.rect.collidepoint(mouse_pos):
                    self.deselect_settlements()
                    self.action = ActionType.PLACE_CITY

                if self.dice1.rect.collidepoint(mouse_pos) \
                        or self.dice2.rect.collidepoint(mouse_pos):
                    self.dice1.roll()
                    self.dice2.roll()
                    self._on_dice_roll(self.dice1.value, self.dice2.value)

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


    def on_update(self):
        self.txt_current_player.update()
        self.txt_current_action.update()


    def on_render(self, screen):
        screen.fill("#65cee0")

        for terrain_tile in self.board.terrain_tiles.values():
            terrain_tile.draw(screen)

        for road in self.board.roads:
            road.draw(screen)

        for settlement in self.board.settlements:
            settlement.draw(screen)

        self.dice1.draw(screen)
        self.dice2.draw(screen)

        self.btn_next_turn.draw(screen)
        self.btn_place_settlement.draw(screen)
        self.btn_place_road.draw(screen)
        self.btn_place_city.draw(screen)

        self.txt_current_player.draw(screen)
        self.txt_current_action.draw(screen)


    def _on_place_road(self, settlement):
        # select first settlement
        if len(self.selected) == 0:
            self.selected.append(settlement)
            settlement.selected = True

        elif len(self.selected) == 1:
            # FIXME: stop players from placing roads over other players
            # settlements??

            # select second settlement.
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
                if (not road_occupied) and (touching_own_road or touching_own_settlement):
                    self.board.add_road(*self.selected, self.current_player)
                    self.current_player.num_roads += 1

                # deselect settlements when road successfully placed
                self.deselect_settlements()

            # deselect the first settlement
            elif settlement == self.selected[0]:
                self.selected[0].selected = False
                self.selected.clear()


    def _on_place_settlement(self, settlement):
        space_around = True
        touching_roads = False
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
        placed_initial = self.current_player.num_settlements >= 2

        # check if settlement is already owned by any player
        already_owned = not isinstance(settlement, EmptySettlement)

        if not already_owned and space_around and (not placed_initial or touching_roads):
            self.board.add_settlement(settlement, self.current_player)
            self.current_player.num_settlements += 1
    

    def _on_place_city(self, settlement):
        if settlement.owner == self.current_player:
            self.board.add_city(settlement)
            self.current_player.num_cities += 1


    def _on_place_robber(self, terrain):
        pass


    def _on_dice_roll(self, num1, num2):
        total = num1 + num2
        # ...
