import unittest
from robber import Robber  

class TestRobber(unittest.TestCase):

    def setUp(self):
        self.robber = Robber()

    def test_set_and_get_hex(self):
        hextile = "A1"  # or any other  value, 
        self.robber.set_hex(hextile)
        self.assertEqual(self.robber.get_hex(), hextile, "Failed to set and get the hextile correctly")

    def test_set_and_get_owner(self):
        owner = "Player 1"  # or any othr  owner value, 
        self.robber.set_owner(owner)
        self.assertEqual(self.robber.get_owner(), owner, "Failed to set and get the owner correctly")


if __name__ == '__main__':
    unittest.main()

