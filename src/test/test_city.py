import unittest
import pygame
from catan.models.city import City
from catan.models.player import Player


class TestCity(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.owner = Player("Player 1", "Color 1")
        self.city = City(0, self.owner)

    def test_init(self):
        # Test City instance creation and the property values
        self.assertIsInstance(self.city, pygame.sprite.Sprite)
        self.assertIsInstance(self.city.image, pygame.Surface)
        self.assertIsInstance(self.city.rect, pygame.Rect)
        self.assertEqual(self.city.value, 0)
        self.assertEqual(self.city.selected, False)
        self.assertEqual(self.city.owner, self.owner)

    def test_set_pos(self):
         # Test the set_pos method by setting the city's position
        self.city.set_pos(50, 50)
        self.assertEqual(self.city.rect.center, (50, 50))

    def test_get_pos(self):
        # Test the get_pos method by retrieving the city's position
        self.city.set_pos(50, 50)
        pos = self.city.get_pos()
        self.assertEqual(pos, (50, 50))

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()