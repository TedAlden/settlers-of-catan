import unittest
import pygame
from catan.models.harbour import Harbour
from catan.type import ResourceType


class TestHarbour(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def test_harbour(self):
        axial_coord = (1, 2)
        resource_type = ResourceType.LUMBER
        node1 = 10
        node2 = 11

        harbour = Harbour(axial_coord, resource_type, node1, node2)

        harbour.set_pos(100, 100)

        self.assertEqual(harbour.get_type(), ResourceType.LUMBER)
        self.assertEqual(harbour.get_trade_ratio(), 2)
        self.assertEqual(harbour.get_connections(), (10, 11))
        self.assertEqual(harbour.get_pos(), (100, 100))

    def test_generic_harbour(self):
        axial_coord = (1, 2)
        resource_type = ResourceType.ANY
        node1 = 10
        node2 = 11

        harbour = Harbour(axial_coord, resource_type, node1, node2)

        harbour.set_pos(100, 100)

        self.assertEqual(harbour.get_type(), ResourceType.ANY)
        self.assertEqual(harbour.get_trade_ratio(), 3)
        self.assertEqual(harbour.get_connections(), (10, 11))
        self.assertEqual(harbour.get_pos(), (100, 100))

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()