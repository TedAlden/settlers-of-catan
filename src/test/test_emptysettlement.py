import unittest
from emptysettlement import EmptySettlement 
from unittest.mock import patch


class TestEmptySettlement(unittest.TestCase):

    def setUp(self):
        with patch("emptysettlement.pygame.sprite.Sprite.__init__"):
            with patch("emptysettlement.pygame.Surface"):
                self.index = 0
                self.empty_settlement = EmptySettlement(self.index)

    def test_set_and_get_pos(self):
        center_x, center_y = 100, 200
        self.empty_settlement.set_pos(center_x, center_y)
        self.assertEqual(self.empty_settlement.get_pos(), (center_x, center_y), "Failed to set and get position correctly")


if __name__ == '__main__':
    unittest.main()

