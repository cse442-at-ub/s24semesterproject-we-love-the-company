import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import unittest
from strike import Strike
from backpack import Backpack
from item import Sword, Potion  # Assuming these are defined with a dice_modifier

class StrikeTest(unittest.TestCase):
    def setUp(self):
        self.strike = Strike()
        self.backpack = Backpack(50)

    def test_initialization(self):
        self.assertIsInstance(self.strike, Strike, "Strike instance is not initialized correctly.")

    def test_backpack_setting(self):
        self.strike.set_player_backpack(self.backpack)
        self.assertEqual(self.strike.player_backpack, self.backpack, "Backpack was not set correctly.")

    def test_combat_outcome_without_items(self):
        self.strike.set_player_backpack(self.backpack)  # An empty backpack
        outcome = self.strike.combat_outcome_with_items('d6', 'd6')
        self.assertIn(outcome, ['player wins', 'enemy wins', 'draw'], "Invalid outcome without items.")

    def test_combat_outcome_with_items(self):
        sword = Sword()
        self.backpack.add(sword)
        self.strike.set_player_backpack(self.backpack)
        
        outcomes = [self.strike.combat_outcome_with_items('d6', 'd6') for _ in range(100)]
        has_player_win = 'player wins' in outcomes
        self.assertTrue(has_player_win, "Player never wins; item effects may not be applied correctly.")

    def test_invalid_die_input(self):
        self.strike.set_player_backpack(self.backpack)  # Setting a backpack (even though it's empty here)
        with self.assertRaises(ValueError):
            self.strike.combat_outcome_with_items('d100', 'd6')

if __name__ == '__main__':
    unittest.main()
