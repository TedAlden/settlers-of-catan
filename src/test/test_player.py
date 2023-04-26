import unittest
from catan.models.board import Board
from catan.models.player import Player
from catan.models.settlement import Settlement



class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Test Player", "Red")
     
     ###---------COUNTS--------###
        
    def test_count_card_knight(self):
        self.player.card_knight = 5
        self.assertEqual(self.player.count_card_knight(), 5)

    def test_count_card_road(self):
        self.player.card_road = 3
        self.assertEqual(self.player.count_card_road(), 3)

    def test_count_card_year_plenty(self):
        self.player.card_year_plenty = 2
        self.assertEqual(self.player.count_card_year_plenty(), 2)

    def test_count_card_monopoly(self):
        self.player.card_monopoly = 1
        self.assertEqual(self.player.count_card_monopoly(), 1)

    def test_count_card_vp(self):
        self.player.card_vp = 4
        self.assertEqual(self.player.count_card_vp(), 4)

    def test_count_settlements(self):
        self.player.settlements = 3
        self.assertEqual(self.player.count_settlements(), 3)

    def test_count_roads(self):
        self.player.roads = 7
        self.assertEqual(self.player.count_roads(), 7)

    def test_count_cities(self):
        self.player.cities = 2
        self.assertEqual(self.player.count_cities(), 2)    
    
    def test_count_resource_cards(self):
        self.player.lumber = 2
        self.player.wool = 3
        self.player.grain = 4
        self.player.brick = 1
        self.player.ore = 5
        self.assertEqual(self.player.count_resource_cards(), 15)

    def test_count_development_cards(self):
        self.player.card_knight = 2
        self.player.card_road = 1
        self.player.card_year_plenty = 3
        self.player.card_monopoly = 1
        self.player.card_vp = 4
        self.assertEqual(self.player.count_development_cards(), 11)
        
        
        ####---------------------------------------------###    

    def test_initial_resources(self):
        self.assertEqual(self.player.count_lumber(), 0)
        self.assertEqual(self.player.count_wool(), 0)
        self.assertEqual(self.player.count_grain(), 0)
        self.assertEqual(self.player.count_brick(), 0)
        self.assertEqual(self.player.count_ore(), 0)

    def test_initial_cards(self):
        self.assertEqual(self.player.count_card_knight(), 0)
        self.assertEqual(self.player.count_card_road(), 0)
        self.assertEqual(self.player.count_card_year_plenty(), 0)
        self.assertEqual(self.player.count_card_monopoly(), 0)
        self.assertEqual(self.player.count_card_vp(), 0)

    def test_initial_structures(self):
        self.assertEqual(self.player.count_settlements(), 0)
        self.assertEqual(self.player.count_cities(), 0)
        self.assertEqual(self.player.count_roads(), 0)

    def test_add_resources(self):
        self.player.add_resources(lumber=2, wool=1, grain=3, brick=0, ore=0)
        self.assertEqual(self.player.count_lumber(), 2)
        self.assertEqual(self.player.count_wool(), 1)
        self.assertEqual(self.player.count_grain(), 3)
        self.assertEqual(self.player.count_brick(), 0)
        self.assertEqual(self.player.count_ore(), 0)

    def test_remove_resources(self):
        self.player.add_resources(lumber=2, wool=1, grain=3, brick=0, ore=0)
        self.player.remove_resources(lumber=1, wool=0, grain=2, brick=0, ore=0)
        self.assertEqual(self.player.count_lumber(), 1)
        self.assertEqual(self.player.count_wool(), 1)
        self.assertEqual(self.player.count_grain(), 1)
        self.assertEqual(self.player.count_brick(), 0)
        self.assertEqual(self.player.count_ore(), 0)

    def test_has_resources(self):
        self.player.add_resources(lumber=2, wool=1, grain=3, brick=0, ore=0)
        self.assertTrue(self.player.has_resources(lumber=1, wool=1, grain=1, brick=0, ore=0))
        self.assertFalse(self.player.has_resources(lumber=2, wool=2, grain=2, brick=0, ore=0))

    def tearDown(self):
        del self.player


    def test_settlement_counter(self):
        # ensure counter increments by 1 after placing settlement
        pass


    def test_city_counter(self):
        # ensure counter increments by 1 after placing city
        pass


    def test_road_counter(self):
        # ensure counter increments by 1 after placing road
        pass


    def test_settlement_resource_requirement(self):
        # player must have the required resources to build a settlement
        pass


    def test_city_resource_requirement(self):
        # player must have the required resources to build a city
        pass


    def test_road_resource_requirement(self):
        # player must have the required resources to build a road
        pass


    def test_city_upgrading_settlement(self):
        # city can not be placed, must be upgraded via a settlement
        pass


    def test_settlement_count_limit(self):
        # player has maximum of 5 settlements
        pass


    def test_road_count_limit(self):
        # player has maximum of 15 roads
        pass


    def test_city_count_limit(self):
        # player has maximum of 4 cities
        pass
      

if __name__ == "__main__":
    unittest.main()