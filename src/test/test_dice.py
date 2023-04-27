import unittest
from dice import Dice  
from unittest.mock import patch


class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_roll(self):
        with patch("dice.random.randint") as mock_randint:
            mock_randint.return_value = 3
            self.dice.roll()
            self.assertEqual(self.dice.value, 3, "Failed to roll the dice and set the correct value")
            mock_randint.assert_called_once_with(1, 6)

    def test_roll_randomness(self):
        roll_values = set()
        for _ in range(1000):
            self.dice.roll()
            roll_values.add(self.dice.value)
        self.assertEqual(len(roll_values), 6, "The dice does not seem to produce all possible values")


if __name__ == '__main__':
    unittest.main()

