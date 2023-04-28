import unittest
from catan.models.dice import Dice  

class TestDice(unittest.TestCase):

    def test_dice_fairness(self):
        # Create a Dice object
        dice = Dice()

        # Number of dice rolls to simulate
        rolls = 1000000

        #  store the count of each outcome (1-6)
        outcomes = {i: 0 for i in range(1, 7)}

        # Roll the dice to the specified number of times and record the outcomes
        for _ in range(rolls):
            dice.roll()
            outcomes[dice.value] += 1

        # Calculate the expected probability for each outcome (assuming fair dice)
        expected_probability = 1 / 6

        # Set a tolerance level for the difference between observed and expected probabilities
        tolerance = 0.01

        # Check if the observed probabilities are within the acceptable tolerance range
        for i in range(1, 7):
            # Calculate the observed probability of each outcome
            outcomes[i] /= rolls

            # Assert that the observed probability is close to the expected probability (within tolerance)
            self.assertAlmostEqual(outcomes[i], expected_probability, delta=tolerance,
                                   msg=f"Outcome {i} has a probability outside the acceptable tolerance.")

if __name__ == '__main__':
    unittest.main()