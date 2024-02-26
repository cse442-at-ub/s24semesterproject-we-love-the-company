import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import unittest
from Combat import Combat  # Adjust the import according to your project structure

class CombatSystemTests(unittest.TestCase):
    def setUp(self):
        self.combat_instance = Combat()  # Create an instance of Combat for use in tests

    def test_roll_die(self):
        for die in self.combat_instance.dice.keys():
            roll = self.combat_instance.roll_die(die)
            self.assertIn(roll, self.combat_instance.dice[die], f"Roll {roll} not in range for {die}")

    def test_combat(self):
        results = set()
        for _ in range(100):
            result = self.combat_instance.combat_outcome('d6', 'd6')
            results.add(result)
        self.assertTrue({'player', 'enemy', 'draw'}.issubset(results), "Not all possible outcomes occurred")

    def test_downgrade_die(self):
        self.assertEqual(self.combat_instance.downgrade_die('d20'), 'd12', "d20 should downgrade to d12")
        self.assertEqual(self.combat_instance.downgrade_die('d4'), 'defeated', "d4 should result in 'defeated'")

    def test_invalid_die_input(self):
        with self.assertRaises(ValueError):
            self.combat_instance.roll_die('d100')  # Use instance to call method

    def test_upgrade_die(self):
        self.assertEqual(self.combat_instance.upgrade_die('d6'), 'd8', "d6 should upgrade to d8")

if __name__ == '__main__':
    unittest.main()

