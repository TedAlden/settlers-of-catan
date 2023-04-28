import unittest
from catan.models.hextile import HexTile

class TestHexTile(unittest.TestCase):

    def setUp(self):
        self.hex_tile = HexTile((0,0))

    def test_init(self):
        self.assertEqual(self.hex_tile.axial_coord, (0,0))
        self.assertEqual(self.hex_tile.radius, 55)
        self.assertIsNone(self.hex_tile.type)
        self.assertEqual(self.hex_tile.number, -1)

    def test_set_pos(self):
        self.hex_tile.set_pos(100, 200)
        self.assertEqual(self.hex_tile.get_pos(), (100, 200))

if __name__ == '__main__':
    unittest.main()