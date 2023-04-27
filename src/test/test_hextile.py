import unittest
from hextile import HexTile  
from unittest.mock import patch


class TestHexTile(unittest.TestCase):

    def setUp(self):
        with patch("hextile.pygame.sprite.Sprite.__init__"):
            with patch("hextile.pygame.Surface"):
                self.axial_coord = (1, 2)
                self.hextile = HexTile(self.axial_coord)

    def test_set_and_get_pos(self):
        center_x, center_y = 100, 200
        self.hextile.set_pos(center_x, center_y)
        self.assertEqual(self.hextile.get_pos(), (center_x, center_y), "Failed to set and get position correctly")


if __name__ == '__main__':
    unittest.main()

