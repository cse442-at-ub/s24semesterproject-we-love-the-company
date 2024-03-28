import random
import os

class Combat:
    def __init__(self):
        # Define the dice and their ranges
        self.dice = {
            'd4': range(1, 5),
            'd6': range(1, 7),
            'd8': range(1, 9),
            'd10': range(1, 11),
            'd12': range(1, 13),
            'd20': range(1, 21),
        }
        # Define the upgrade and downgrade paths for combat dice
        self.upgrade_path = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
        # Reverse of upgrade_path for downgrade
        self.downgrade_path = self.upgrade_path[::-1]

        icons_path = os.path.join(os.path.dirname(__file__), "Assets", "dice_icons")
        self.icon_map = {
            'd4': os.path.join(icons_path, "d4.png"),
            'd6': os.path.join(icons_path, "d6.png"),
            'd8': os.path.join(icons_path, "d8.png"),
            'd10': os.path.join(icons_path, "d10.png"),
            'd12': os.path.join(icons_path, "d12.png"),
            'd20': os.path.join(icons_path, "d20.png"),
        }

    def get_icon_path(self, die):
        if die not in self.icon_map:
            raise ValueError(f"{die} is not a valid die.")

        return self.icon_map[die]

    def roll_die(self, die):
        """Rolls the specified die and returns the result."""
        if die not in self.dice:
            raise ValueError(f"{die} is not a valid die.")
        return random.choice(list(self.dice[die]))

    def outcome(self, player_roll, enemy_roll):
        if player_roll > enemy_roll:
            return 'player'
        elif enemy_roll > player_roll:
            return 'enemy'
        else:
            return 'draw'

    def combat_outcome(self, player_die, enemy_die):
        """Simulates combat between player and enemy, returning the outcome."""
        player_roll = self.roll_die(player_die)
        enemy_roll = self.roll_die(enemy_die)

        return self.outcome(player_roll, enemy_roll)
    
    def downgrade_die(self, current_die):
        """Downgrades the die type, or marks as defeated if already at lowest."""
        if current_die == self.downgrade_path[-1]:  # 'd4' should be the last element in the reversed list
            return 'defeated'
        else:
            current_index = self.downgrade_path.index(current_die)
            return self.downgrade_path[current_index + 1]  # Move one step down in the downgrade path

    def upgrade_die(self, current_die):
        """Upgrades the die type, or remains the same if already at highest."""
        if current_die == self.upgrade_path[-1]:  # 'd20' is the last element
            return current_die  # Cannot upgrade further
        else:
            return self.upgrade_path[self.upgrade_path.index(current_die) + 1]
