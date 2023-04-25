import unittest

from catan.models.bank import Bank


class TestBank(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()


    def test_count_resources(self):
        self.assertEqual(self.bank.count_lumber(), 19)
        self.assertEqual(self.bank.count_wool(), 19)
        self.assertEqual(self.bank.count_grain(), 19)
        self.assertEqual(self.bank.count_brick(), 19)
        self.assertEqual(self.bank.count_ore(), 19)


    def test_count_development_cards(self):
        self.assertEqual(self.bank.count_development_cards(), 25)


    def test_has_resources(self):
        self.assertTrue(self.bank.has_resources(lumber=1, wool=1))
        self.assertFalse(self.bank.has_resources(lumber=20))


    def test_add_resources(self):
        self.bank.add_resources(lumber=1, wool=2, grain=3)
        self.assertEqual(self.bank.count_lumber(), 20)
        self.assertEqual(self.bank.count_wool(), 21)
        self.assertEqual(self.bank.count_grain(), 22)


    def test_remove_resources(self):
        self.bank.remove_resources(lumber=1, wool=2, grain=3)
        self.assertEqual(self.bank.count_lumber(), 18)
        self.assertEqual(self.bank.count_wool(), 17)
        self.assertEqual(self.bank.count_grain(), 16)

        # Test if resources go below 0
        self.bank.remove_resources(lumber=20)
        self.assertEqual(self.bank.count_lumber(), 0)


if __name__ == '__main__':
    unittest.main()
