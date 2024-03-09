import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")
from combat import Combat
from backpack import Backpack
from item import Item, Sword, Shield, Potion, Boots  


class Strike(Combat):
    def __init__(self):
        super().__init__()
        self.player_backpack = None  # Initialize player_backpack here 

    def set_player_backpack(self, backpack):
        """Set the player's backpack to be considered in combat calculations."""
        if not isinstance(backpack, Backpack):
            raise ValueError("Invalid backpack. Must be an instance of Backpack.")
        self.player_backpack = backpack

    def roll_die_with_modifiers(self, die):
        base_roll = super().roll_die(die)
        modifiers = 0
        if self.player_backpack:
            # Ensure you're accessing item instances that have a `dice_modifier` attribute
            modifiers = sum(item.dice_modifier for item in self.player_backpack.items if hasattr(item, 'dice_modifier'))
        return base_roll + modifiers

    def combat_outcome_with_items(self, player_die, enemy_die):
        """Calculates the combat outcome considering items in the player's backpack."""
        player_roll = self.roll_die_with_modifiers(player_die)
        enemy_roll = super().roll_die(enemy_die)  # Enemy roll does not consider player's items

        if player_roll > enemy_roll:
            return 'player wins'
        elif player_roll < enemy_roll:
            return 'enemy wins'
        else:
            return 'draw'

