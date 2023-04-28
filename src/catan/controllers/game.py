"""Module containing game controller for the Catan board game.

This module contains the `GameController` class which is part of an MVC
architecture. It works as an interface between the game view and the game
model, to abstract complexity and improve maintainability.

Typical usage example:
    ```
    from catan.models.game import GameModel
    model = GameModel()
    controller = GameController(model)
    ```
"""

from catan.models.bank import Bank
from catan.models.dice import Dice
from catan.models.emptysettlement import EmptySettlement
from catan.models.game import GameModel
from catan.models.hextile import HexTile
from catan.models.player import Player
from catan.models.road import Road
from catan.models.robber import Robber
from catan.models.settlement import Settlement
from catan.models.city import City
from catan.type import ActionType, TerrainType


class GameController:
    """The game controller class.

    The game controller makes up part of an MVC architecture, and works
    on wrapping a game model object.

    Attributes:
        model:
            The game model being controlled.
        action:
            The current game action being performed, e.g. placing a settlement.
    """

    def __init__(
            self,
            model: GameModel
        ) -> None:
        """Initialize the game controller.

        Args:
            model:
                The game model to be controlled.
        """
        self.model = model
        self.action = ActionType.NONE

        # TODO:
        # player_already_rolled = False
        # player_robber_placed = False
        # player_roads_placed = 0  # how many roads placed this turn
        # player_settlements_placed = 0
        # player_cities_placed = 0

        # self.turn_number = 0
        # self.round_number = 0


    def get_robber(
            self
        ) -> Robber:
        """
        """
        return self.model.robber
    
    
    def get_dice(
            self
        ) -> tuple[Dice]:
        """
        """
        return self.model.dice1, self.model.dice2


    def get_bank(
            self
        ) -> Bank:
        """
        """
        return self.model.bank


    def get_players(
            self
        ) -> list[Player]:   # list[Player | AIPlayer]
        """
        """
        return self.model.players


    def get_current_player(
            self
        ) -> Player:
        """Gets the pointer to the current player taking their turn.
        """
        return self.model.current_turn
    

    def set_current_player(
            self,
            player: Player
        ) -> None:
        """Sets the pointer to the current player taking their turn.

        Args:
            player:
                The player taking to be taking their turn.
        """
        self.model.current_turn = player


    def get_roads(
            self
        ) -> list[Road]:
        """
        """
        return self.model.board.roads


    def get_settlements(
            self
        ) -> list[EmptySettlement | Settlement | City]:
        """
        """
        return self.model.board.settlements


    def get_tiles(
            self
        ) -> list[HexTile]:
        """
        """
        return self.model.board.terrain_tiles.values()
    

    def get_harbours(self):
        return self.model.board.harbours.values()
    

    def is_turn_finished(
            self
        ) -> bool:
        """
        """

        # TODO
        
        pass


    def next_turn(
            self
        ) -> None:
        """Ready the game state and starts the next players turn in sequence.

        The next player will be the next in order, wrapping to the start of the
        sequence. I.e. player 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, ...
        """
        # Skip to the next turn in order

        # TODO: if on first round, go in reverse order

        increment = 1 # if round == 1 or round > 2 else -1
        players = self.get_players()
        idx = players.index(self.get_current_player())
        idx = (idx + increment) % len(players)
        self.set_current_player(players[idx])
        print(f"Player turn: {self.get_current_player().name}")

        # reset variables, i.e. player_has_rolled_dice = False etc...


    def place_road(
            self,
            settlement1: EmptySettlement | Settlement | City,
            settlement2: EmptySettlement | Settlement | City
        ) -> None:
        """Place a road between `settlement1` and `settlement2`.

        Performs the placement if the correct game criteria are met:
            - The player must have sufficient resources.
            - The road must be adjacent to one of the players existing pieces
            - The road must be placed between two adjacent nodes.
            - The road must not already exist.

        Args:
            settlement1:
                The first of the two settlements to place the road in between.
            settlement2:
                The second of the two settlements to place the road in between.
        """
        afford = self.get_current_player().has_resources(brick=1,
                                                         lumber=1)
        
        # two initial roads are free
        placed_initial = self.get_current_player().count_roads() >= 2

        # check that both nodes are adjancent
        if settlement2 in self.model.board.get_surrounding_nodes(settlement1):
            # check if touching one of the players existing roads
            touching_own_road = False
            for node in (settlement1, settlement2):
                for road in self.model.board.roads:
                    if road.owner == self.get_current_player() and node in road.settlements:
                        touching_own_road = True

            # check if touching one of the players existing settlements
            touching_own_settlement = False
            if self.get_current_player() in (settlement1.owner, settlement2.owner):
                touching_own_settlement = True

            # check that the road does not already exist
            road_occupied = self.model.board.has_road(settlement1, settlement2)

            # finally place road if all conditions are valid
            if (not road_occupied) and (touching_own_road or touching_own_settlement):
                if not placed_initial or (placed_initial and afford):
                    self.model.board.add_road(settlement1, settlement2, self.get_current_player())
                    self.get_current_player().roads += 1
                    print(f"Player '{self.get_current_player().name}' placed a road!")

                    if placed_initial:
                        self.get_current_player().remove_resources(brick=1,
                                                                   lumber=1)


    def place_settlement(
            self,
            settlement: EmptySettlement
        ) -> None:
        """Place a settlement on a vertex on the board.

        Performs the placement if the correct game criteria are met:
            - The player must have sufficient resources.
            - The vertex must not have any existing settlements.
            - The settlement can not be adjacent to another settlement.
            - The settlement must be adjacent to one of the players existing
              settlements or roads, unless it is one of the initial two being
              placed.

        Args:
            settlement:
                The settlement marker to place the settlement on.
        """

        afford = self.get_current_player().has_resources(brick=1,
                                                         lumber=1,
                                                         wool=1,
                                                         grain=1)

        # check if settlement is already owned by any player
        already_owned = isinstance(settlement, (Settlement, City))
        # check if this is one of the players initial 2 settlements
        placed_initial = self.get_current_player().count_settlements() >= 2
        space_around = True
        touching_roads = False
        for node in self.model.board.get_surrounding_nodes(settlement):
            # check there are no adjacent settlements already
            if isinstance(node, Settlement) or isinstance(node, City):
                space_around = False

            # check the settlement is touching one of the players roads
            for road in self.model.board.roads:
                if settlement in road.settlements and node in road.settlements:
                    touching_roads = True

        # finally place settlement if all conditions are valid
        if not already_owned and space_around and (not placed_initial or touching_roads):
            if not placed_initial or (placed_initial and afford):
                self.model.board.add_settlement(settlement, self.get_current_player())
                self.get_current_player().settlements += 1
                print(f"Player '{self.get_current_player().name}' placed a settlement!")#

                if placed_initial:
                    self.get_current_player().remove_resources(brick=1,
                                                               lumber=1,
                                                               wool=1,
                                                               grain=1)


    def place_city(
            self,
            settlement: Settlement
        ) -> None:
        """Upgrade an existing settlement to a city.

        Performs the placement if the correct game criteria are met:
            - The player must have sufficient resources.
            - The settlement must exist and belong to the same player.

        Args:
            settlement:
                The settlement to upgrade to a city.
        """

        afford = self.get_current_player().has_resources(ore=3,
                                                         grain=2)

        # check player is upgrading their own settlement to a city
        if settlement.owner == self.get_current_player() and afford:
            # perform upgrade
            self.model.board.add_city(settlement)
            self.get_current_player().cities += 1
            print(f"Player '{self.get_current_player().name}' upgraded to a city!")



    def place_robber(
            self,
            hextile: HexTile
        ) -> None:
        """Move the robber to a given hex tile.

        Moves the game robber to the chosen hex tile and sets the robber's
        ownership to the current player.

        Args:
            hextile:
                The hex tile to move the robber to.
        """
        self.get_robber().set_hex(hextile)
        self.get_robber().set_owner(self.get_current_player())
        print(f"Player '{self.get_current_player().name}' placed the robber!")


    def roll_dice(
            self
        ) -> None:
        """Roll the game dice and distribute resources.

        Rolls the two game dice and distributes resources to the settlements
        on any hextiles with a matching number. If a 7 is rolled, then the
        current player can place the robber.
        """
        dice1, dice2 = self.get_dice()
        bank = self.get_bank()

        dice1.roll()
        dice2.roll()
        total = dice1.value + dice2.value

        current_player = self.get_current_player().name

        turn_info = f"{current_player} rolled a {total}\n"

        if total == 7:
            self.action = ActionType.PLACE_ROBBER
            turn_info += f"{current_player} can place the robber!\n"

        for terrain_tile in self.get_tiles():
            if terrain_tile.number == total:
                for settlement in self.model.board.get_surrounding_nodes(terrain_tile):
                    if isinstance(settlement, (Settlement, City)):
                        collector = settlement.owner
                        robber = self.get_robber()
                        if terrain_tile == robber.get_hex():
                            collector = self.get_robber().get_owner()
                            robber_owner = robber.get_owner().name
                            turn_info += f"{robber_owner} has the robber here!\n"

                        # receive double resources if city, else 1
                        amount = 2 if isinstance(settlement, City) else 1
                        name = collector.name

                        if terrain_tile.type == TerrainType.FOREST:
                            if bank.has_resources(lumber=amount):
                                collector.add_resources(lumber=amount)
                                bank.remove_resources(lumber=amount)
                                turn_info += f"Given '{name}' {amount}x lumber\n"

                        elif terrain_tile.type == TerrainType.PASTURE:
                            if bank.has_resources(wool=amount):
                                collector.add_resources(wool=amount)
                                bank.remove_resources(wool=amount)
                                turn_info += f"Given '{name}' {amount}x wool\n"

                        elif terrain_tile.type == TerrainType.FIELD:
                            if bank.has_resources(grain=amount):
                                collector.add_resources(grain=amount)
                                bank.remove_resources(grain=amount)
                                turn_info += f"Given '{name}' {amount}x grain\n"

                        elif terrain_tile.type == TerrainType.HILL:
                            if bank.has_resources(brick=amount):
                                collector.add_resources(brick=amount)
                                bank.remove_resources(brick=amount)
                                turn_info += f"Given '{name}' {amount}x brick\n"

                        elif terrain_tile.type == TerrainType.MOUNTAIN:
                            if bank.has_resources(ore=amount):
                                collector.add_resources(ore=amount)
                                bank.remove_resources(ore=amount)
                                turn_info += f"Given '{name}' {amount}x ore\n"

        print(turn_info)
