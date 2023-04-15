from catan.models.settlement import Settlement
from catan.models.emptysettlement import EmptySettlement
from catan.models.city import City
from catan.type import ActionType, TerrainType


class GameController:

    def __init__(self, model):
        self.model = model
        self.action = ActionType.NONE
        self.current_player = self.model.players[0]

        # TODO:
        # ... = BankController
        # ... = DiceController

        # player_already_rolled = False
        # player_robber_placed = False
        # player_roads_placed = 0  # how many roads placed this turn
        # player_settlements_placed = 0
        # player_cities_placed = 0

        # self.turn_number = 0
        # self.round_number = 0


    def get_robber(self):
        return self.model.robber
    
    
    def get_dice(self):
        return self.model.dice1, self.model.dice2


    def get_bank(self):
        return self.model.bank


    def get_players(self):
        return self.model.players


    def get_current_player(self):
        return self.current_player


    def get_roads(self):
        return self.model.board.roads


    def get_settlements(self):
        return self.model.board.settlements


    def get_tiles(self):
        return self.model.board.terrain_tiles.values()


    def next_turn(self):
        # Skip to the next turn in order
        players = self.get_players()
        idx = players.index(self.current_player)
        idx = (idx + 1) % len(players)
        self.current_player = players[idx]
        print(f"Player turn: {self.current_player.name}")


    def place_road(self, settlement1, settlement2):
        # check that both nodes are adjancent
        if settlement2 in self.model.board.get_surrounding_nodes(settlement1):
            # check if touching one of the players existing roads
            touching_own_road = False
            for node in (settlement1, settlement2):
                for road in self.model.board.roads:
                    if road.owner == self.current_player and node in road.settlements:
                        touching_own_road = True

            # check if touching one of the players existing settlements
            touching_own_settlement = False
            if self.current_player in (settlement1.owner, settlement2.owner):
                touching_own_settlement = True

            # check that the road does not already exist
            road_occupied = self.model.board.has_road(settlement1, settlement2)

            # finally place road if all conditions are valid
            if (not road_occupied) and (touching_own_road or touching_own_settlement):
                self.model.board.add_road(settlement1, settlement2, self.current_player)
                self.current_player.roads += 1
                print(f"Player '{self.current_player.name}' placed a road!")


    def place_settlement(self, settlement):
        # check if settlement is already owned by any player
        already_owned = isinstance(settlement, (Settlement, City))
        # check if this is one of the players initial 2 settlements
        placed_initial = self.current_player.count_settlements() >= 2
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
            self.model.board.add_settlement(settlement, self.current_player)
            self.current_player.settlements += 1
            print(f"Player '{self.current_player.name}' placed a settlement!")


    def place_city(self, settlement):
        # check player is upgrading their own settlement to a city
        if settlement.owner == self.current_player:
            # perform upgrade
            self.model.board.add_city(settlement)
            self.current_player.cities += 1
            print(f"Player '{self.current_player.name}' upgraded to a city!")


    def place_robber(self, terrain):
        self.get_robber().set_hex(terrain)
        self.get_robber().set_owner(self.current_player)
        print(f"Player '{self.current_player.name}' placed the robber!")


    def roll_dice(self):
        dice1, dice2 = self.get_dice()
        bank = self.get_bank()

        dice1.roll()
        dice2.roll()
        total = dice1.value + dice2.value

        turn_info = f"{self.current_player.name} rolled a {total}\n"

        if total == 7:
            self.action = ActionType.PLACE_ROBBER


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
